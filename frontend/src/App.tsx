// src/App.tsx
import ChatContainer from './components/ChatContainer';
import './App.css';
import SideNav from './components/SideNav';

function App() {
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
