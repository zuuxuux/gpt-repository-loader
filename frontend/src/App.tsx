// src/App.tsx
import ChatContainer from './components/ChatContainer'
import { NavBar } from './components/NavBar'
import TopicCard from './components/TopicCard'
import { mockTopics } from './data/topics'
import './App.css'

function App() {
  return (
    <div>
      <div className="container mx-auto">
        <ChatContainer />
      </div>
      <div className="container mx-auto grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mt-8">
        {mockTopics.map((topic, index) => (
          <TopicCard
            key={index}
            topic={topic}
            onThumbsUp={() => console.log(`Liked: ${topic.title}`)}
            onThumbsDown={() => console.log(`Disliked: ${topic.title}`)}
          />
        ))}
      </div>
    </div>
  )
}

export default App