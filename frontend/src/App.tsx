// src/App.tsx
import ChatContainer from './components/ChatContainer'
import { NavBar } from './components/NavBar'
import TopicCard from './components/TopicCard'
import { mockTopics } from './data/topics'
import './App.css'

// If you’re using the modular approach from earlier, 
// import SideNav from "@/components/ui/SideNav/SideNav" (or wherever you put it).
import SideNav from '@/components/SideNav'  

function App() {
  return (
    <div className="flex">
      {/* MAIN CONTENT ON THE LEFT */}
      <div className="flex-1">
        {/* Existing content */}
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

      {/* SIDENAV ON THE RIGHT */}
      <SideNav />
    </div>
  )
}

export default App
