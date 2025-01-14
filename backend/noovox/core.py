from abc import ABC, abstractmethod
import requests
from bs4 import BeautifulSoup
import time
from typing import List, Dict, Optional
import re
from urllib.parse import urlparse, quote
import random
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
import sys
import os
from openai import OpenAI
from fuzzywuzzy import fuzz
from noovox.constants import General, Keys
import logging


class BaseAgent:
    def __init__(self, name, agent_role, agent_knowledge_base, model=General.DEFAULT_MODEL,
                 api_key=os.getenv(Keys.OPEN_AI_KEY)):
        self.__name = name
        self.__agent_role = agent_role
        self.__knowledge_base = self.load_knowledge_base(agent_knowledge_base)
        self.__client = OpenAI(api_key=api_key)  # Initialize OpenAI client
        self.__model = model  # Set the OpenAI model
        self.__history = []  # To store chat history

    @staticmethod
    def load_knowledge_base(path):
        """Load knowledge base content as text."""
        if not os.path.exists(path):
            return []
        with open(path, "r") as file:
            return file.readlines()

    def __calculate_relevance(self, query):
        """Use fuzzy matching to calculate relevance score with the knowledge base."""
        scores = [fuzz.partial_ratio(query.lower(), kb.lower()) for kb in self.__knowledge_base]
        return max(scores, default=0)

    def ask_openai(self, prompt, temperature=0.2):
        """
        Query OpenAI with a prompt, including filtered history for context.
        """
        # Add the system message for context
        system_message = {"role": "system", "content": f"You are an expert in {self.__agent_role}."}

        # Filter chat history to include the most recent messages
        filtered_chat_history = [system_message] + self.__history[-10:]  # Limit to last 10 exchanges
        filtered_chat_history.append({"role": "user", "content": prompt})

        # Use the OpenAI client to get a response
        response = self.__client.chat.completions.create(
            model=self.__model,
            messages=filtered_chat_history,
            temperature=temperature,
        )
        response_content = response.choices[0].message.content

        # Update the history with the assistant's response
        self.__history.append({"role": "user", "content": prompt})
        self.__history.append({"role": "assistant", "content": response_content})

        return response_content

    def __process_query(self, query):
        """
        Process a query by calculating relevance and using OpenAI for a response.
        """
        relevance_score = self.__calculate_relevance(query)
        prompt = f"Answer as an expert in {self.__agent_role} with a relevance score of {relevance_score}: {query}"
        return {
            "response": self.ask_openai(prompt),
            "relevance_score": relevance_score
        }


class ManagerAgent:
    def __init__(self, employees):
        self.employees = employees
        self.feedback_log = {}  # Store feedback from users

        # Configure logging
        logging.basicConfig(filename="agent_log.log", level=logging.INFO)

    def route_query(self, query):
        responses = []
        for employee in self.employees:
            logging.info(f"Routing query to {employee.name}")
            result = employee.__process_query(query)
            responses.append({
                "agent": employee.name,
                "response": result["response"],
                "relevance_score": result["relevance_score"]
            })

        # Rank responses by relevance score
        best_response = max(responses, key=lambda x: x["relevance_score"])
        return {
            "best_response": best_response,
            "all_responses": responses
        }

    def log_feedback(self, agent_name, feedback):
        """Log user feedback for a specific agent."""
        if agent_name not in self.feedback_log:
            self.feedback_log[agent_name] = []
        self.feedback_log[agent_name].append(feedback)
        logging.info(f"Feedback for {agent_name}: {feedback}")


class NoovoxSearcher:
    """
    NewsSearcher is a comprehensive tool for searching and extracting news articles
    from various online sources. It handles HTTP requests, parses HTML content,
    and provides an interactive user interface for querying and displaying results.
    """

    @dataclass
    class ContentSource:
        """
        Data class representing a news content source.

        Attributes:
            name (str): The name of the news source.
            url (str): The URL template for searching articles.
            type (str): The type of the content source (e.g., 'search').
            category (str): The category of news (e.g., 'news', 'general').
            language (str): The language of the content. Defaults to 'en'.
        """
        name: str
        url: str
        type: str
        category: str
        language: str = 'en'

    def __init__(self):
        """
        Initializes the NewsSearcher with user agents, settings, and news sources.

        This constructor sets up user agent rotation to mimic natural browsing,
        defines retry and timeout settings for HTTP requests, initializes
        a list of news sources categorized under 'news' and 'general',
        and configures logging.
        """
        self.configure_logging()
        self.logger = logging.getLogger(self.__class__.__name__)

        # Rotate user agents to look more natural
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'
        ]

        # Content extraction settings
        self.max_retries = 3
        self.timeout = 10
        self.max_threads = 5  # Limit concurrent requests

        # Define news sources
        self.sources = self.initialize_sources()

        # Define common article patterns for content extraction
        self.content_patterns = {
            'article': ['article', 'main', '.article-body', '.story-content', '#article-body', '.post-content'],
            'title': ['h1', 'h2', 'h3', '.title', '.headline'],
            'description': ['.description', '.summary', '.excerpt', 'p'],
            'content': ['p'],
        }

    @property
    def __tqdm(self):
        # Optional: For better output formatting
        try:
            from tqdm import tqdm
            return tqdm
        except ImportError:
            return

    @property
    def __tabulate(self):
        # Optional: For better output formatting
        try:
            from tabulate import tabulate
            return tabulate
        except ImportError:
            return

    def configure_logging(self):
        """
        Configures logging with both console and file handlers.
        """
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)

        # Formatter
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        # File Handler
        file_handler = logging.FileHandler('news_scraper.log', mode='a')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        # Console Handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    def initialize_sources(self) -> Dict[str, List[ContentSource]]:
        """
        Initializes and returns the dictionary of news sources categorized under 'news' and 'general'.

        Returns:
            Dict[str, List[ContentSource]]: A dictionary with categories as keys and lists of ContentSource objects as values.
        """
        return {
            'news': [
                NoovoxSearcher.ContentSource(
                    name='Google News',
                    url='https://news.google.com/search?q={query}&hl=en-US&gl=US&ceid=US:en',
                    type='search',
                    category='news'
                ),
                NoovoxSearcher.ContentSource(
                    name='Bing News',
                    url='https://www.bing.com/news/search?q={query}',
                    type='search',
                    category='news'
                ),
                NoovoxSearcher.ContentSource(
                    name='Yahoo News',
                    url='https://news.search.yahoo.com/search?p={query}',
                    type='search',
                    category='news'
                ),
            ],
            'general': [
                NoovoxSearcher.ContentSource(
                    name='Google News',
                    url='https://news.google.com/search?q={query}&hl=en-US&gl=US&ceid=US:en',
                    type='search',
                    category='general'
                ),
                NoovoxSearcher.ContentSource(
                    name='Bing News',
                    url='https://www.bing.com/news/search?q={query}',
                    type='search',
                    category='general'
                ),
                NoovoxSearcher.ContentSource(
                    name='Yahoo News',
                    url='https://news.search.yahoo.com/search?p={query}',
                    type='search',
                    category='general'
                ),
                NoovoxSearcher.ContentSource(
                    name='Reuters',
                    url='https://www.reuters.com/search/news?blob={query}',
                    type='search',
                    category='general'
                ),
                NoovoxSearcher.ContentSource(
                    name='Financial Times',
                    url='https://www.ft.com/search?q={query}',
                    type='search',
                    category='general'
                )
            ]
        }

    def get_random_user_agent(self) -> str:
        """
        Selects a random user agent string from the predefined list.

        Returns:
            str: A randomly selected user agent string.
        """
        return random.choice(self.user_agents)

    def get_headers(self) -> Dict[str, str]:
        """
        Generates HTTP request headers with a randomized User-Agent.

        Returns:
            Dict[str, str]: A dictionary of HTTP headers.
        """
        return {
            'User-Agent': self.get_random_user_agent(),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }

    def search_news(self, query: str, category: str = 'general') -> List[Dict]:
        """
        Initiates the search for news articles based on a query and category.

        This method orchestrates the fetching of articles from multiple sources
        concurrently, filters the results for relevance, and extracts full content.

        Args:
            query (str): The search query string.
            category (str): The category of news to search within.

        Returns:
            List[Dict]: A list of dictionaries containing article data.
        """
        self.logger.info(f"Starting search for: '{query}' in category: '{category}'")
        all_results = []

        # Validate category
        if category not in self.sources:
            self.logger.warning(f"Unknown category '{category}', defaulting to 'general'.")
            category = 'general'

        # Use tqdm for progress indication if available
        executor = ThreadPoolExecutor(max_workers=self.max_threads)
        futures = {
            executor.submit(self.fetch_articles_from_source, source, query): source
            for source in self.sources[category]
        }

        if self.__tqdm:
            progress = self.__tqdm(as_completed(futures), total=len(futures), desc="Fetching articles")
        else:
            progress = as_completed(futures)

        for future in progress:
            source = futures[future]
            try:
                articles = future.result()
                if articles:
                    all_results.extend(articles)
                    self.logger.info(f"Found {len(articles)} articles from '{source.name}'")
            except Exception as e:
                self.logger.error(f"Error fetching articles from '{source.name}': {str(e)}")

        executor.shutdown(wait=True)

        # Filter and sort results
        filtered_results = self.filter_results(all_results, query)
        self.logger.info(f"Total relevant articles after filtering: {len(filtered_results)}")

        # Extract full content
        if filtered_results:
            self.logger.info("Extracting full content from articles...")
            filtered_results = self.extract_full_content(filtered_results)
        else:
            self.logger.info("No articles to extract content from.")

        return filtered_results

    def fetch_articles_from_source(self, source: ContentSource, query: str) -> List[Dict]:
        """
        Fetches articles from a specific news source based on the search query.

        This method constructs the search URL, makes the HTTP request, and
        parses the returned HTML to extract article information.

        Args:
            source (ContentSource): The content source to fetch articles from.
            query (str): The search query string.

        Returns:
            List[Dict]: A list of dictionaries containing article data from the source.
        """
        try:
            url = source.url.format(query=quote(query))
            self.logger.debug(f"Fetching articles from URL: {url}")
            response = self.make_request(url)
            if response:
                return self.extract_articles(response.text, url, source)
        except Exception as e:
            self.logger.error(f"Exception occurred while fetching articles from '{source.name}': {str(e)}")
        return []

    def make_request(self, url: str, retry_count: int = 0) -> Optional[requests.Response]:
        """
        Makes an HTTP GET request to the specified URL with retry logic.

        This method attempts to fetch the content from the URL, handling retries
        with exponential backoff in case of failures.

        Args:
            url (str): The URL to fetch.
            retry_count (int): The current retry attempt count.

        Returns:
            Optional[requests.Response]: The HTTP response object if successful, else None.
        """
        try:
            response = requests.get(
                url,
                headers=self.get_headers(),
                timeout=self.timeout,
                allow_redirects=True
            )
            response.raise_for_status()
            self.logger.debug(f"Successfully fetched URL: {url}")
            return response
        except requests.RequestException as e:
            if retry_count < self.max_retries:
                self.logger.warning(f"Request failed ({retry_count + 1}/{self.max_retries}): {url} | Error: {str(e)}")
                time.sleep(2 ** retry_count)  # Exponential backoff
                return self.make_request(url, retry_count + 1)
            else:
                self.logger.error(f"Request failed after {self.max_retries} retries: {url}")
                return None

    def extract_articles(self, html: str, url: str, source: ContentSource) -> List[Dict]:
        """
        Parses the HTML content to extract article information based on the source.

        Depending on the news source, a specific parsing method is invoked to
        accurately extract article details.

        Args:
            html (str): The HTML content of the page.
            url (str): The URL of the source.
            source (ContentSource): The content source object.

        Returns:
            List[Dict]: A list of dictionaries containing extracted article data.
        """
        articles = []
        soup = BeautifulSoup(html, 'html.parser')

        # Choose parsing method based on source
        parser_method = self.get_parser_method(url)
        if parser_method:
            articles = parser_method(soup)
            self.logger.debug(f"Parsed {len(articles)} articles using {parser_method.__name__}")
        else:
            articles = self.parse_generic(soup)
            self.logger.debug(f"Parsed {len(articles)} articles using generic parser")

        # Add source information
        for article in articles:
            article['source'] = source.name
            article['category'] = source.category

        return articles

    def get_parser_method(self, url: str):
        """
        Determines the appropriate parser method based on the URL.

        Args:
            url (str): The URL to determine the parser for.

        Returns:
            Callable: The parser method if found, else None.
        """
        if 'google' in url:
            return self.parse_google_news
        elif 'bing' in url:
            return self.parse_bing_news
        elif 'yahoo' in url:
            return self.parse_yahoo_news
        elif 'reuters' in url:
            return self.parse_reuters
        elif 'ft.com' in url:
            return self.parse_ft
        else:
            return self.parse_generic

    def parse_generic(self, soup: BeautifulSoup) -> List[Dict]:
        """
        Parses HTML content using generic patterns to extract articles.

        This method attempts to find articles by searching for common HTML tags
        and class names that are typically used to structure news articles.

        Args:
            soup (BeautifulSoup): The BeautifulSoup object of the HTML content.

        Returns:
            List[Dict]: A list of dictionaries containing extracted article data.
        """
        articles = []

        # Find articles using common patterns
        article_elements = (
                soup.find_all('article') +
                soup.find_all(class_=re.compile(r'article|post|story|news-item', re.I)) +
                soup.find_all(['div', 'section'], class_=re.compile(r'article|post|story|news-item', re.I))
        )

        for article in article_elements:
            try:
                # Find title
                title_elem = None
                for selector in ['h1', 'h2', 'h3', 'h4', '.title', '.headline']:
                    title_elem = article.select_one(selector)
                    if title_elem:
                        break

                # Find link
                link_elem = article.find('a', href=True)

                if title_elem and link_elem:
                    url = link_elem['href']
                    url = self.normalize_url(url)

                    # Find description
                    desc_elem = None
                    for selector in ['.description', '.summary', '.excerpt', 'p']:
                        desc_elem = article.select_one(selector)
                        if desc_elem:
                            break

                    articles.append({
                        'title': title_elem.get_text().strip(),
                        'url': url,
                        'description': desc_elem.get_text().strip() if desc_elem else '',
                        'published': ''
                    })
            except Exception as e:
                self.logger.error(f"Error parsing generic article: {str(e)}")
                continue

        return articles

    def parse_google_news(self, soup: BeautifulSoup) -> List[Dict]:
        """
        Parses HTML content from Google News to extract articles.

        This method specifically targets the structure used by Google News
        to list articles, extracting titles, URLs, and publication times.

        Args:
            soup (BeautifulSoup): The BeautifulSoup object of the HTML content.

        Returns:
            List[Dict]: A list of dictionaries containing extracted article data.
        """
        articles = []
        for article in soup.find_all('article'):
            try:
                title_elem = article.find('h3')
                link_elem = article.find('a', href=True)
                time_elem = article.find('time')

                if title_elem and link_elem:
                    url = link_elem['href']
                    url = self.normalize_url(url, base='https://news.google.com')

                    published = time_elem['datetime'] if time_elem and time_elem.has_attr('datetime') else ''

                    articles.append({
                        'title': title_elem.get_text().strip(),
                        'url': url,
                        'description': '',
                        'published': published
                    })
            except Exception as e:
                self.logger.error(f"Error parsing Google News article: {str(e)}")
                continue
        return articles

    def parse_bing_news(self, soup: BeautifulSoup) -> List[Dict]:
        """
        Parses HTML content from Bing News to extract articles.

        This method specifically targets the structure used by Bing News
        to list articles, extracting titles, URLs, and descriptions.

        Args:
            soup (BeautifulSoup): The BeautifulSoup object of the HTML content.

        Returns:
            List[Dict]: A list of dictionaries containing extracted article data.
        """
        articles = []
        for article in soup.find_all('div', class_=re.compile(r'news-card', re.I)):
            try:
                title_elem = article.find('a', class_=re.compile(r'title', re.I))
                desc_elem = article.find('div', class_=re.compile(r'snippet', re.I))

                if title_elem and title_elem.has_attr('href'):
                    url = title_elem['href']
                    url = self.normalize_url(url)

                    articles.append({
                        'title': title_elem.get_text().strip(),
                        'url': url,
                        'description': desc_elem.get_text().strip() if desc_elem else '',
                        'published': ''
                    })
            except Exception as e:
                self.logger.error(f"Error parsing Bing News article: {str(e)}")
                continue
        return articles

    def parse_yahoo_news(self, soup: BeautifulSoup) -> List[Dict]:
        """
        Parses HTML content from Yahoo News to extract articles.

        This method specifically targets the structure used by Yahoo News
        to list articles, extracting titles, URLs, and descriptions.

        Args:
            soup (BeautifulSoup): The BeautifulSoup object of the HTML content.

        Returns:
            List[Dict]: A list of dictionaries containing extracted article data.
        """
        articles = []
        for article in soup.find_all(['div', 'article'], class_=re.compile(r'NewsArticle|stream-item', re.I)):
            try:
                title_elem = article.find(['h2', 'h3', 'h4']) or article.find('a', class_=re.compile(r'title|headline',
                                                                                                     re.I))
                link_elem = article.find('a', href=True)

                if title_elem and link_elem:
                    url = link_elem['href']
                    url = self.normalize_url(url, base='https://news.yahoo.com')

                    desc_elem = article.find(['p', 'div'], class_=re.compile(r'description|summary', re.I))

                    articles.append({
                        'title': title_elem.get_text().strip(),
                        'url': url,
                        'description': desc_elem.get_text().strip() if desc_elem else '',
                        'published': ''
                    })
            except Exception as e:
                self.logger.error(f"Error parsing Yahoo News article: {str(e)}")
                continue
        return articles

    def parse_reuters(self, soup: BeautifulSoup) -> List[Dict]:
        """
        Parses HTML content from Reuters to extract articles.

        This method specifically targets the structure used by Reuters
        to list articles, extracting titles, URLs, and descriptions.

        Args:
            soup (BeautifulSoup): The BeautifulSoup object of the HTML content.

        Returns:
            List[Dict]: A list of dictionaries containing extracted article data.
        """
        articles = []
        for article in soup.find_all('div', class_=re.compile(r'search-result-content', re.I)):
            try:
                title_elem = article.find('h3')
                link_elem = article.find('a', href=True)
                desc_elem = article.find('p')

                if title_elem and link_elem:
                    url = link_elem['href']
                    url = self.normalize_url(url, base='https://www.reuters.com')

                    articles.append({
                        'title': title_elem.get_text().strip(),
                        'url': url,
                        'description': desc_elem.get_text().strip() if desc_elem else '',
                        'published': ''
                    })
            except Exception as e:
                self.logger.error(f"Error parsing Reuters article: {str(e)}")
                continue
        return articles

    def parse_ft(self, soup: BeautifulSoup) -> List[Dict]:
        """
        Parses HTML content from Financial Times to extract articles.

        This method specifically targets the structure used by Financial Times
        to list articles, extracting titles, URLs, and descriptions.

        Args:
            soup (BeautifulSoup): The BeautifulSoup object of the HTML content.

        Returns:
            List[Dict]: A list of dictionaries containing extracted article data.
        """
        articles = []
        for article in soup.find_all('div', class_=re.compile(r'o-teaser__content', re.I)):
            try:
                title_elem = article.find('a', class_=re.compile(r'js-teaser-heading-link', re.I))
                desc_elem = article.find('p', class_=re.compile(r'o-teaser__standfirst', re.I))

                if title_elem and title_elem.has_attr('href'):
                    url = title_elem['href']
                    url = self.normalize_url(url, base='https://www.ft.com')

                    articles.append({
                        'title': title_elem.get_text().strip(),
                        'url': url,
                        'description': desc_elem.get_text().strip() if desc_elem else '',
                        'published': ''
                    })
            except Exception as e:
                self.logger.error(f"Error parsing Financial Times article: {str(e)}")
                continue
        return articles

    def normalize_url(self, url: str, base: Optional[str] = None) -> str:
        """
        Normalizes the URL by resolving relative paths.

        Args:
            url (str): The URL to normalize.
            base (Optional[str]): The base URL to use for resolving relative URLs.

        Returns:
            str: The normalized absolute URL.
        """
        if url.startswith('//'):
            return f"https:{url}"
        elif url.startswith('/'):
            if base:
                parsed_base = urlparse(base)
                return f"{parsed_base.scheme}://{parsed_base.netloc}{url}"
            else:
                return url  # Cannot resolve without base
        elif not url.startswith('http'):
            return f"https://{url}"
        return url

    def filter_results(self, results: List[Dict], query: str) -> List[Dict]:
        """
        Filters and sorts the list of articles based on their relevance to the query.

        Articles are scored based on the presence of query terms in their titles
        and descriptions. Higher relevance scores indicate a better match.

        Args:
            results (List[Dict]): The list of articles to filter.
            query (str): The search query string.

        Returns:
            List[Dict]: A sorted list of articles with relevance scores.
        """
        filtered = []
        seen_urls = set()
        query_terms = query.lower().split()

        for result in results:
            url = result.get('url', '')
            title = result.get('title', '').lower()
            description = result.get('description', '').lower()

            if url and url not in seen_urls:
                # Calculate relevance score
                relevance = 0
                for term in query_terms:
                    if term in title:
                        relevance += 2  # Title matches are weighted more
                    if term in description:
                        relevance += 1

                if relevance > 0:
                    seen_urls.add(url)
                    result['relevance_score'] = relevance
                    filtered.append(result)

        # Sort by relevance score
        sorted_results = sorted(filtered, key=lambda x: x.get('relevance_score', 0), reverse=True)
        self.logger.debug(f"Filtered and sorted results, total {len(sorted_results)} articles")
        return sorted_results

    def extract_full_content(self, articles: List[Dict]) -> List[Dict]:
        """
        Extracts the full textual content and images from each article.

        This method fetches the full article pages concurrently and parses
        the main content, extracting paragraphs and image URLs.

        Args:
            articles (List[Dict]): The list of articles to extract content from.

        Returns:
            List[Dict]: A list of articles enriched with full text and images.
        """
        articles_with_content = []
        self.logger.info("Starting extraction of full content from articles.")

        # Use tqdm for progress indication if available
        if self.__tqdm:
            executor = ThreadPoolExecutor(max_workers=self.max_threads)
            futures = {
                executor.submit(self.fetch_full_article_content, article): article
                for article in articles
            }
            progress = self.__tqdm(as_completed(futures), total=len(futures), desc="Extracting content")
        else:
            executor = ThreadPoolExecutor(max_workers=self.max_threads)
            futures = {
                executor.submit(self.fetch_full_article_content, article): article
                for article in articles
            }
            progress = as_completed(futures)

        for future in progress:
            article = futures[future]
            try:
                full_article = future.result()
                if full_article:
                    articles_with_content.append(full_article)
            except Exception as e:
                self.logger.error(f"Error extracting full content for '{article['title']}': {str(e)}")

        executor.shutdown(wait=True)
        self.logger.info(f"Completed extraction of content. {len(articles_with_content)} articles enriched.")
        return articles_with_content

    def fetch_full_article_content(self, article: Dict) -> Optional[Dict]:
        """
        Fetches and extracts the full content from a specific article URL.

        This method retrieves the article's webpage, removes unwanted elements,
        and extracts the main text and image URLs.

        Args:
            article (Dict): The article dictionary containing at least the 'url'.

        Returns:
            Optional[Dict]: The article dictionary enriched with 'full_text',
                            'text_length', and 'images' if successful, else None.
        """
        try:
            self.logger.debug(f"Fetching full content from URL: {article['url']}")
            response = self.make_request(article['url'])
            if not response:
                return None

            soup = BeautifulSoup(response.text, 'html.parser')

            # Remove unwanted elements
            for elem in soup.find_all(['script', 'style', 'nav', 'header', 'footer', 'aside']):
                elem.decompose()

            # Find main content
            content = None
            for selector in self.content_patterns['article']:
                content = soup.select_one(selector)
                if content:
                    break

            if not content:
                self.logger.warning(f"Main content not found for URL: {article['url']}")
                return None

            # Extract paragraphs
            paragraphs = []
            for p in content.find_all('p'):
                text = p.get_text().strip()
                if len(text) > 50:  # Filter out short paragraphs
                    paragraphs.append(text)

            if not paragraphs:
                self.logger.warning(f"No substantial paragraphs found for URL: {article['url']}")
                return None

            # Extract images
            images = content.find_all('img', src=True)
            image_urls = []
            for img in images:
                src = img['src']
                if src:
                    src = self.normalize_url(src, base=article['url'])
                    image_urls.append(src)

            # Update article with full content
            article['full_text'] = '\n\n'.join(paragraphs)
            article['text_length'] = sum(len(p) for p in paragraphs)
            article['images'] = image_urls[:5]  # Limit to 5 images

            self.logger.debug(f"Successfully extracted content from '{article['title']}'")
            return article

        except Exception as e:
            self.logger.error(f"Exception occurred while extracting content from '{article['url']}': {str(e)}")
            return None

    def return_results(self, articles: List[Dict], query: str, export_format: Optional[str] = None,
                       export_data: bool = False) -> Dict:
        """
        Structures the articles data into a dictionary format for output and optionally exports to a file.

        This method organizes the articles along with metadata such as the
        total count and the original query. It also exports the data to a specified format if requested.

        Args:
            articles (List[Dict]): The list of articles to include in the output.
            query (str): The search query string.
            export_format (Optional[str]): The format to export the results ('json' or 'csv'). Defaults to None.

        Returns:
            Dict: A dictionary containing the status, message, data, and optionally the exported file name.
        """
        # Initialize the base result structure
        result_data = {
            "status": "success",
            "message": "Articles retrieved successfully" if articles else "No articles found",
            "data": {
                "articles": articles,
                "article_count": len(articles),
                "query": query
            }
        }

        # Proceed only if an export format is specified
        if export_data and export_format:
            export_format = export_format.lower()

            # Validate the export format
            if export_format not in ['json', 'csv']:
                self.logger.error(f"Unsupported export format: {export_format}")
                result_data['exported_file'] = None
                return result_data

            # Generate a timestamped filename
            timestamp = int(time.time())
            filename = f"news_results_{timestamp}.{export_format}"

            try:
                if export_format == 'json':
                    # Export the results to a JSON file
                    with open(filename, 'w', encoding='utf-8') as f:
                        json.dump(result_data, f, ensure_ascii=False, indent=4)
                    self.logger.info(f"Results exported to JSON file: {filename}")
                    result_data['exported_file'] = filename

                elif export_format == 'csv':
                    # Handle empty articles list
                    if not articles:
                        self.logger.warning("No articles to export to CSV.")
                        result_data['exported_file'] = None
                    else:
                        import csv
                        # Extract CSV headers from article keys
                        keys = articles[0].keys()
                        with open(filename, 'w', newline='', encoding='utf-8') as f:
                            dict_writer = csv.DictWriter(f, fieldnames=keys)
                            dict_writer.writeheader()
                            dict_writer.writerows(articles)
                        self.logger.info(f"Results exported to CSV file: {filename}")
                        result_data['exported_file'] = filename

            except Exception as e:
                self.logger.error(f"Error exporting results to {export_format}: {str(e)}")
                result_data['exported_file'] = None

        return result_data

    def format_article_preview(self, article: Dict, max_preview_length: int = 200) -> str:
        """
        Formats an article's details into a readable preview string.

        This preview includes the title, source, publication date, content length,
        a text preview, URL, and the number of images.

        Args:
            article (Dict): The article dictionary containing various details.
            max_preview_length (int): The maximum length of the text preview.

        Returns:
            str: A formatted string containing the article's preview.
        """
        preview = [
            f"Title: {article.get('title', 'N/A')}",
            f"Source: {article.get('source', 'N/A')} ({article.get('category', 'N/A')})",
        ]

        if article.get('published'):
            preview.append(f"Published: {article.get('published')}")

        if article.get('text_length'):
            preview.append(f"Content Length: {article.get('text_length')} characters")

        if article.get('full_text'):
            text_preview = article['full_text'][:max_preview_length]
            if len(article['full_text']) > max_preview_length:
                text_preview += "..."
            preview.append(f"Preview: {text_preview}")

        preview.append(f"URL: {article.get('url', 'N/A')}")

        if article.get('images'):
            preview.append(f"Images: {len(article['images'])} found")

        return '\n'.join(preview)

    def run(self):
        """
        Executes the main interactive loop for searching and displaying articles.

        This method provides a command-line interface where users can input search
        queries and categories, view article previews, and access full article content.
        It handles user inputs, displays results, and manages the search workflow.
        """
        self.display_welcome_message()

        while True:
            try:
                query = self.get_user_input("\nEnter search query (or 'quit' to exit): ").strip()
                if query.lower() == 'quit':
                    break

                # Get category with validation
                category = self.get_user_input("\nEnter category (news/general) [default: general]: ").strip().lower()
                if not category:
                    category = 'general'
                elif category not in ['news', 'general']:
                    print("Invalid category. Defaulting to 'general'.")
                    category = 'general'

                print(f"\nSearching for articles about '{query}' in category '{category}'...")
                print("Please wait while we fetch the articles...\n")

                results = self.search_news(query, category)

                if results:
                    print(f"\nFound {len(results)} relevant articles with full content.\n")

                    # Export options
                    export_choice = self.get_user_input(
                        "Would you like to export the results? (json/csv/n): ").strip().lower()
                    if export_choice in ['json', 'csv']:
                        filename = self.return_results(results, query, export_format=export_choice)
                        if filename:
                            print(f"Results exported to: {filename}")
                    else:
                        self.logger.info("Export skipped by user.")

                    # Show detailed previews of top results
                    top_n = min(5, len(results))
                    print(f"\nTop {top_n} articles:")
                    for i, article in enumerate(results[:top_n], 1):
                        print(f"\nArticle {i}:")
                        print(self.format_article_preview(article))

                    # Offer to show more results
                    if len(results) > top_n:
                        show_more = self.get_user_input("\nWould you like to see more results? (y/n): ").strip().lower()
                        if show_more == 'y':
                            additional_n = min(5, len(results) - top_n)
                            for i, article in enumerate(results[top_n:top_n + additional_n], top_n + 1):
                                print(f"\nArticle {i}:")
                                print(self.format_article_preview(article))

                    # Offer to display full content for a specific article
                    while True:
                        article_num = self.get_user_input(
                            "\nEnter article number to see full content (or 'c' to continue): ").strip().lower()
                        if article_num == 'c':
                            break
                        elif article_num.isdigit():
                            idx = int(article_num) - 1
                            if 0 <= idx < len(results):
                                selected_article = results[idx]
                                print("\nFull article content:")
                                print("=" * 60)
                                print(selected_article.get('full_text', 'No content available.'))
                                print("=" * 60)
                                if selected_article.get('images'):
                                    print("\nImage URLs:")
                                    for img_url in selected_article['images']:
                                        print(img_url)
                            else:
                                print("Invalid article number.")
                        else:
                            print("Invalid input. Please enter a number or 'c' to continue.")
                else:
                    print("\nNo relevant articles found.")
                    print("Tips:")
                    print("- Try using fewer or different keywords")
                    print("- Check for typos in your search terms")
                    print("- Try a different category")

                continue_search = self.get_user_input(
                    "\nWould you like to search for something else? (y/n): ").strip().lower()
                if continue_search != 'y':
                    break

            except KeyboardInterrupt:
                print("\n\nSearch interrupted by user.")
                break
            except Exception as e:
                self.logger.error(f"Unexpected error in main loop: {str(e)}")
                print(f"\nAn unexpected error occurred: {str(e)}")
                retry = self.get_user_input("Would you like to try again? (y/n): ").strip().lower()
                if retry != 'y':
                    break

        print("\nThank you for using the News Article Search Tool!")

    def display_welcome_message(self):
        """
        Displays a welcome message to the user.
        """
        welcome = """
============================================
 News Article Search and Content Extraction Tool
============================================
        """
        print(welcome)

    def get_user_input(self, prompt: str) -> str:
        """
        Handles user input with proper exception handling.

        Args:
            prompt (str): The prompt message to display to the user.

        Returns:
            str: The user's input.
        """
        try:
            return input(prompt)
        except EOFError:
            self.logger.warning("EOFError encountered. Exiting input loop.")
            return 'quit'
        except KeyboardInterrupt:
            self.logger.warning("KeyboardInterrupt encountered during input.")
            return 'quit'

    def main(self):
        """
        Entry point for the NewsSearcher tool.

        This method starts the interactive search interface. It also handles
        any fatal errors by logging them and notifying the user.
        """
        try:
            self.run()
        except Exception as e:
            self.logger.error(f"Fatal error: {str(e)}")
            print(f"\nFatal error: {str(e)}")
            print("Check the log file for details.")



class LLMProvider(ABC):
    """
    Abstract base class for LLM providers.
    Subclasses must implement the __call__ method.
    """
    @abstractmethod
    def __call__(self, input_message: str) -> str:
        """
        Process input message and return LLM response.
        
        Args:
            input_message (str): The input text to send to the LLM
            
        Returns:
            str: The LLM's response text
        """
        pass


class OpenAIProvider(LLMProvider):
    """
    OpenAI implementation of LLMProvider.
    Supports configuration via constructor and per-call parameters.
    
    Args:
        api_key (str, optional): OpenAI API key. Defaults to OPENAI_KEY environment variable.
        model (str, optional): Model to use. Defaults to "gpt-4".
        temperature (float, optional): Sampling temperature. Defaults to 0.2.
        **kwargs: Additional parameters to pass to OpenAI API.
    """
    def __init__(self, 
                 api_key: str = None,
                 model: str = "gpt-4o-mini",
                 temperature: float = 0.2,
                 **kwargs):
        try:
            import openai
            import os
            
            # Use provided API key or fall back to environment variable
            self.api_key = api_key or os.getenv('OPENAI_KEY')
            if not self.api_key:
                raise ValueError("No API key provided and OPENAI_KEY environment variable not set")
            
            self.client = openai.OpenAI(api_key=self.api_key)
            self.default_model = model
            self.default_temperature = temperature
            self.default_kwargs = kwargs
            
        except ImportError:
            raise ImportError("OpenAI package not installed. Run: pip install openai")
        except Exception as e:
            raise Exception(f"Failed to initialize OpenAI client: {str(e)}")

    def __call__(self, 
                 input_message: str,
                 model: str = None,
                 temperature: float = None,
                 **kwargs) -> str:
        """
        Send message to OpenAI API and return response.
        
        Args:
            input_message (str): Message to send to OpenAI
            model (str, optional): Override default model for this call
            temperature (float, optional): Override default temperature for this call
            **kwargs: Additional parameters to override defaults for this call
            
        Returns:
            str: Response from OpenAI
        """
        try:
            # Merge default and call-specific parameters
            call_kwargs = self.default_kwargs.copy()
            call_kwargs.update(kwargs)
            
            response = self.client.chat.completions.create(
                model=model or self.default_model,
                temperature=temperature or self.default_temperature,
                messages=[{
                    "role": "user",
                    "content": input_message
                }],
                **call_kwargs
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"OpenAI API call failed: {str(e)}")


class DummyProvider(LLMProvider):
    """
    Dummy implementation of LLMProvider that simply echoes back a formatted version
    of the input message. Useful for testing and development.
    """
    def __call__(self, input_message: str) -> str:
        """
        Returns a simple formatted response containing the input message.
        
        Args:
            input_message (str): Any input message
            
        Returns:
            str: A formatted response containing the input message
        """
        return f"Responding to: {input_message}"