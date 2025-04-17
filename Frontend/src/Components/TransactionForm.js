import React, { useState, useEffect } from 'react';

const TransactionForm = ({ addTransaction, categories, defaultCategory }) => {
  const [description, setDescription] = useState('');
  const [amount, setAmount] = useState('');
  const [category, setCategory] = useState(defaultCategory || categories[0]);

  // Update category if defaultCategory changes
  useEffect(() => {
    if (defaultCategory) {
      setCategory(defaultCategory);
    }
  }, [defaultCategory]);

  const handleSubmit = (e) => {
    e.preventDefault();
    
    const amountNum = parseFloat(amount);
    
    if (description.trim() !== '' && !isNaN(amountNum)) {
      const newTransaction = {
        id: Math.floor(Math.random() * 1000000),
        description,
        amount: amountNum,
        category,
        date: new Date().toISOString()
      };
      
      addTransaction(newTransaction);
      setDescription('');
      setAmount('');
    }
  };

  return (
    <div className="transaction-form">
      <h2>Add New Transaction</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <input
            type="text"
            placeholder="Description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            required
          />
        </div>
        <div className="form-group">
          <input
            type="number"
            placeholder="Amount (use - for expenses)"
            value={amount}
            onChange={(e) => setAmount(e.target.value)}
            required
          />
        </div>
        <div className="form-group">
          <select 
            value={category} 
            onChange={(e) => setCategory(e.target.value)}
            className="category"
          >
            {categories.map((cat) => (
              <option key={cat} value={cat}>{cat}</option>
            ))}
          </select>
        </div>
        <button type="submit">Add Transaction</button>
      </form>
    </div>
  );
};

export default TransactionForm;
