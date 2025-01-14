import { useEffect, useState } from 'react';
import './App.css';
import SideNav from './components/SideNav';
import ChatContainer from './components/ChatContainer';
import { getUser } from '@/lib/utils';
import { User } from '@/lib/types';

function App() {
  const [user, setUser] = useState<User | null>(null);

  useEffect(() => {
    async function initUser() {
      try {
        // Example: create user "John Doe" once on startup
        const newUser = await getUser('John Doe', 'john.doe@example.com');
        setUser(newUser);
      } catch (error) {
        console.error('Error creating user:', error);
      }
    }

    initUser();
  }, []);

  return (
    <div className="appContainer">
      {/* Main Content and Nav */}
      <div className="mainContent">
        {/* Chat Section */}
        <div className="chatContainer">
          <ChatContainer />
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
