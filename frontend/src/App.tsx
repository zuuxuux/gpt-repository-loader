import { useEffect, useState } from 'react';
import './App.css';
import SideNav from './components/SideNav';
import ChatContainer from './components/ChatContainer';
import { getUser, getChatForUser } from '@/lib/utils';
import { User, Chat } from '@/lib/types';

function App() {
  const [user, setUser] = useState<User | null>(null);
  const [chat, setChat] = useState<Chat | null>(null);

  useEffect(() => {
    async function initUserAndChat() {
      try {
        // 1) Get or create user
        const foundUser = await getUser('John Doe', 'john.doe@example.com');
        setUser(foundUser);

        // 2) Now that we have a user, get or create a chat
        const foundChat = await getChatForUser(foundUser.user_id);
        setChat(foundChat);
      } catch (error) {
        console.error('Error initializing user or chat:', error);
      }
    }

    initUserAndChat();
  }, []);

  return (
    <div className="appContainer">
      {/* Main Content and Nav */}
      <div className="mainContent">
        {/* Chat Section */}
        <div className="chatContainer">
        <ChatContainer chat={chat} userId={user?.user_id} />
        </div>

        {/* Topic Cards Section (Optional) */}
        {/* <div className="topicsGrid">
          {mockTopics.map((topic, index) => (
            <TopicCard
              key={index}
              topic={topic}
              onThumbsUp={() => console.log(`Liked: ${topic.title}`)}
              onThumbsDown={() => console.log(`Disliked: ${topic.title}`)}
            />
          ))}
        </div> */}
      </div>

      {/* Side Navigation */}
      <div className="sideNav">
        <SideNav />
      </div>
    </div>
  );
}

export default App;
