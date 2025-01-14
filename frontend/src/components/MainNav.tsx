import styles from './MainNav.module.css';
import { MessageSquare, User, Settings } from 'lucide-react';

interface MainNavProps {
  activeMain: 'chat' | 'user' | 'settings';
  setActiveMain: (val: 'chat' | 'user' | 'settings') => void;
}

export default function MainNav({ activeMain, setActiveMain }: MainNavProps) {
  return (
    <div className={styles.mainNav}>
      <button
        className={`${styles.mainNavItem} ${activeMain === 'chat' ? styles.mainNavItemActive : ''}`}
        onClick={() => setActiveMain('chat')}
        aria-label="Chat"
      >
        <MessageSquare size={24} />
      </button>
      <button
        className={`${styles.mainNavItem} ${activeMain === 'user' ? styles.mainNavItemActive : ''}`}
        onClick={() => setActiveMain('user')}
        aria-label="User"
      >
        <User size={24} />
      </button>
      <button
        className={`${styles.mainNavItem} ${activeMain === 'settings' ? styles.mainNavItemActive : ''}`}
        onClick={() => setActiveMain('settings')}
        aria-label="Settings"
      >
        <Settings size={24} />
      </button>
    </div>
  );
}
