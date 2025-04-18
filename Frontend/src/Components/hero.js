import React from 'react';

const Hero = ({ totalBudget = 1000, categoriesCount = 5 }) => {
  const scrollToContent = () => {
    window.scrollTo({ top: window.innerHeight, behavior: 'smooth' });
  };

  return (
    <header className="hero">
      <div className="hero-content">
        <div className="hero-buttons">
          <button onClick={scrollToContent} className="primary-btn">Manage Budget</button>
          <button onClick={scrollToContent} className="secondary-btn">View Transactions</button>
          <button onClick={() => {}} className="secondary-btn">Login</button>
        </div>
        <div className="hero-stats">
          <div className="stat-item">
            <span className="stat-number">{categoriesCount}</span>
            <span className="stat-label">Budget Categories</span>
          </div>
          <div className="stat-item">
            <span className="stat-number">${totalBudget.toFixed(2)}</span>
            <span className="stat-label">Total Budget</span>
          </div>
          <div className="stat-item">
            <span className="stat-number">27</span>
            <span className="stat-label">Brotherhood Size</span>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Hero;
