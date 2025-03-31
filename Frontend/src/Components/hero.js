import React from 'react';

const Hero = () => {
  const scrollToContent = () => {
    window.scrollTo({ top: window.innerHeight, behavior: 'smooth' });
  };

  return (
    <header className="hero">
      <div className="hero-content">
        <h1>Finance Management System</h1>
        <p>Efficiently manage your organization's budgets across departments with our powerful tracking tools.</p>
        <div className="hero-buttons">
          <button onClick={scrollToContent} className="primary-btn">Get Started</button>
          <button onClick={scrollToContent} className="secondary-btn">Learn More</button>
        </div>
        <div className="hero-stats">
          <div className="stat-item">
            <span className="stat-number">5</span>
            <span className="stat-label">Budget Categories</span>
          </div>
          <div className="stat-item">
            <span className="stat-number">100%</span>
            <span className="stat-label">Transparency</span>
          </div>
          <div className="stat-item">
            <span className="stat-number">24/7</span>
            <span className="stat-label">Access</span>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Hero;
