import React from 'react';

const Hero = () => {
  const scrollToContent = () => {
    window.scrollTo({ top: window.innerHeight, behavior: 'smooth' });
  };

  return (
    <header className="hero">
      <div className="hero-content">
        <h1>Finance Management System</h1>
        <p>Track transactions, manage budgets, and control your inventory seamlessly.</p>
        <button onClick={scrollToContent}>Learn More</button>
      </div>
    </header>
  );
};

export default Hero;
