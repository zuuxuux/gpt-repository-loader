import { useState } from 'react';
import styles from './SideNav.module.css';
import MainNav from '@/components/MainNav';
import SubNav from '@/components/SubNav';

export default function SideNav() {
  // Which main nav item is currently selected
  const [activeMain, setActiveMain] = useState<'chat' | 'user' | 'settings'>('chat');
  // Which sub nav item is currently selected (relevant only if activeMain === 'chat')
  const [activeSub, setActiveSub] = useState<'data' | 'postCreator' | 'postAnalysis'>('data');

  // For demonstration, show sub nav only when 'chat' is selected
  const showSubNav = activeMain === 'chat';

  // Renders the main content depending on states
  let content: JSX.Element;
  if (activeMain === 'chat') {
    switch (activeSub) {
      case 'postCreator':
        content = <div>Post Creator Pane</div>;
        break;
      case 'postAnalysis':
        content = <div>Post Analysis Pane</div>;
        break;
      case 'data':
      default:
        content = <div>Data Pane</div>;
        break;
    }
  } else if (activeMain === 'user') {
    content = <div>User Pane</div>;
  } else {
    content = <div>Settings Pane</div>;
  }

  return (
    <div className={styles.sideNavContainer}>
      {/* Main Nav */}
      <MainNav
        activeMain={activeMain}
        setActiveMain={setActiveMain}
      />

      {/* Sub Nav (only if activeMain === 'chat') */}
      {showSubNav && (
        <SubNav
          activeSub={activeSub}
          setActiveSub={setActiveSub}
        />
      )}

      {/* Main Content (shifted if sub nav is shown) */}
      <div 
        className={
          `${styles.mainContent} ${showSubNav ? styles.offsetLeft : ''}`
        }
      >
        {content}
      </div>
    </div>
  );
}
