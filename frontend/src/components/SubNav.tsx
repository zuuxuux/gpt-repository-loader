import React from 'react';
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
        Data
      </button>
      <button
        className={`${styles.subNavItem} ${activeSub === 'postCreator' ? styles.subNavItemActive : ''}`}
        onClick={() => setActiveSub('postCreator')}
      >
        Post Creator
      </button>
      <button
        className={`${styles.subNavItem} ${activeSub === 'postAnalysis' ? styles.subNavItemActive : ''}`}
        onClick={() => setActiveSub('postAnalysis')}
      >
        Post Analysis
      </button>
    </div>
  );
}
