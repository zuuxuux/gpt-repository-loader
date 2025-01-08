import React from 'react';
import { MessageSquare } from 'lucide-react';
import styles from './SubNav.module.css';

interface SubNavProps {
  activeSub: 'data' | 'postCreator' | 'postAnalysis';
  setActiveSub: (val: 'data' | 'postCreator' | 'postAnalysis') => void;
}

export default function SubNav({ activeSub, setActiveSub }: SubNavProps) {
  return (
    <div className={styles.subNav}>
      <button
        className={`${styles.subNavItem} ${activeSub === 'data' ? styles.subNavItemActive : ''}`}
        onClick={() => setActiveSub('data')}
      >
        <MessageSquare size={16} className={styles.icon} />
        Data
      </button>
      <button
        className={`${styles.subNavItem} ${activeSub === 'postCreator' ? styles.subNavItemActive : ''}`}
        onClick={() => setActiveSub('postCreator')}
      >
        <MessageSquare size={16} className={styles.icon} />
        Post Creator
      </button>
      <button
        className={`${styles.subNavItem} ${activeSub === 'postAnalysis' ? styles.subNavItemActive : ''}`}
        onClick={() => setActiveSub('postAnalysis')}
      >
        <MessageSquare size={16} className={styles.icon} />
        Post Analysis
      </button>
    </div>
  );
}
