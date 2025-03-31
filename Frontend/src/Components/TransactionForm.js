import React, { useState } from 'react';

const TransactionForm = ({ addTransaction, categories }) => {
  const [description, setDescription] = useState('');
  const [amount, setAmount] = useState('');
  const [category, setCategory] = useState(categories[0]);

  const handleSubmit = (e) => {
    e.preventDefault();
    const parsedAmount = parseFloat(amount);
    if (description && !isNaN(parsedAmount) && category) {
      const newTransaction = {
        id: Date.now(),
        description,
        amount: parsedAmount,
        category,
      };
      addTransaction(newTransaction);
      setDescription('');
      setAmount('');
      setCategory(categories[0]);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="transaction-form">
      <h2>Add Transaction</h2>
      <input
        type="text"
        placeholder="Description (e.g., Rent, Salary)"
        value={description}
        onChange={(e) => setDescription(e.target.value)}
        required
      />
      <input
        type="number"
        placeholder="Amount (negative for expense)"
        value={amount}
        onChange={(e) => setAmount(e.target.value)}
        required
      />
      <select 
        value={category} 
        onChange={(e) => setCategory(e.target.value)}
        required
      >
        {categories.map((cat) => (
          <option key={cat} value={cat}>
            {cat}
          </option>
        ))}
      </select>
      <button type="submit">Add Transaction</button>
    </form>
  );
};

export default TransactionForm;
