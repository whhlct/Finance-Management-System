import React, { useState } from 'react';

const BudgetControl = ({ budgets, totalBudget, adjustBudget, categories }) => {
  const [customAmount, setCustomAmount] = useState('');
  const [selectedCategory, setSelectedCategory] = useState(categories[0]);

  const handleCustomAdjust = (e) => {
    e.preventDefault();
    const amount = parseFloat(customAmount);
    if (!isNaN(amount)) {
      adjustBudget(selectedCategory, amount);
      setCustomAmount('');
    }
  };

  return (
    <div className="control-section">
      <h2>Budget Control</h2>
      <p>Total Budget: ${totalBudget.toFixed(2)}</p>
      
      <div className="budget-categories">
        <h3>Budget Categories</h3>
        {categories.map(category => (
          <div key={category} className="budget-category">
            <span>{category}: ${budgets[category].toFixed(2)}</span>
          </div>
        ))}
      </div>
      
      <form onSubmit={handleCustomAdjust} className="custom-adjust">
        <select 
          value={selectedCategory} 
          onChange={(e) => setSelectedCategory(e.target.value)}
        >
          {categories.map((cat) => (
            <option key={cat} value={cat}>
              {cat}
            </option>
          ))}
        </select>
        <input
          type="number"
          placeholder="Enter amount"
          value={customAmount}
          onChange={(e) => setCustomAmount(e.target.value)}
          required
        />
        <button type="submit">Adjust Budget</button>
      </form>
      
      <div className="button-group">
        <button onClick={() => adjustBudget(selectedCategory, -100)}>
          - Decrease {selectedCategory} Budget by $100
        </button>
        <button onClick={() => adjustBudget(selectedCategory, 100)}>
          + Increase {selectedCategory} Budget by $100
        </button>
      </div>
    </div>
  );
};

export default BudgetControl;
