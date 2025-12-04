import React from 'react';
import type { TabType } from '../types';
import './TabBar.css';

interface TabBarProps {
  activeTab: TabType;
  onTabChange: (tab: TabType) => void;
}

const TabBar: React.FC<TabBarProps> = ({ activeTab, onTabChange }) => {
  const tabs: { id: TabType; label: string; icon: string }[] = [
    { id: 'chat', label: 'Chat & Generate', icon: '💬' },
    { id: 'cookbook', label: 'Recipe Cookbook', icon: '📚' },
  ];

  return (
    <div className="tab-bar">
      {tabs.map((tab) => (
        <button
          key={tab.id}
          className={`tab ${activeTab === tab.id ? 'active' : ''}`}
          onClick={() => onTabChange(tab.id)}
        >
          <span className="tab-icon">{tab.icon}</span>
          <span>{tab.label}</span>
        </button>
      ))}
    </div>
  );
};

export default TabBar;
