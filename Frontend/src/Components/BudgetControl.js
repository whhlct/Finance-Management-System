import React, { useState } from 'react';

const BudgetControl = ({ budget, adjustBudget }) => {
  const [customAmount, setCustomAmount] = useState('');

  const handleCustomAdjust = (e) => {
    e.preventDefault();
    const amount = parseFloat(customAmount);
    if (!isNaN(amount)) {
      adjustBudget(amount);
      setCustomAmount('');
    }
  };

  return (
    <div className="control-section">
      <h2>Budget Control</h2>
      <p>Current Budget: ${budget.toFixed(2)}</p>
      <div className="button-group">
        <button onClick={() => adjustBudget(-100)}>- Decrease Budget by $100</button>
        <button onClick={() => adjustBudget(100)}>+ Increase Budget by $100</button>
      </div>
      <form onSubmit={handleCustomAdjust} className="custom-adjust">
        <input
          type="number"
          placeholder="Enter custom amount"
          value={customAmount}
          onChange={(e) => setCustomAmount(e.target.value)}
        />
        <button type="submit">Adjust Budget</button>
      </form>
    </div>
  );
};

export default BudgetControl;
