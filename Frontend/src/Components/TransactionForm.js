import React, { useState } from 'react';

const TransactionForm = ({ addTransaction }) => {
  const [description, setDescription] = useState('');
  const [amount, setAmount] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    const parsedAmount = parseFloat(amount);
    if (description && !isNaN(parsedAmount)) {
      const newTransaction = {
        id: Date.now(),
        description,
        amount: parsedAmount,
      };
      addTransaction(newTransaction);
      setDescription('');
      setAmount('');
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
      />
      <input
        type="number"
        placeholder="Amount (negative for expense)"
        value={amount}
        onChange={(e) => setAmount(e.target.value)}
      />
      <button type="submit">Add Transaction</button>
    </form>
  );
};

export default TransactionForm;
