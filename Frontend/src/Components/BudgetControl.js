import React, { useState } from 'react';

const BudgetControl = () => {
  const [budget, setBudget] = useState(1000);

  const increaseBudget = () => {
    setBudget(budget + 100);
  };

  const decreaseBudget = () => {
    if (budget - 100 >= 0) setBudget(budget - 100);
  };

  return (
    <div className="control-section">
      <h2>Budget Control</h2>
      <p>Current Budget: ${budget.toFixed(2)}</p>
      <div className="button-group">
        <button onClick={decreaseBudget}>- Decrease Budget</button>
        <button onClick={increaseBudget}>+ Increase Budget</button>
      </div>
    </div>
  );
};

export default BudgetControl;
