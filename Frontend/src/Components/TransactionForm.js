import React, { useState, useEffect } from 'react';
import { createTransaction } from '../services/api';
import { getAccounts } from '../services/api';

const TransactionForm = ({ onTransactionCreated }) => {
  const [description, setDescription] = useState('');
  const [amount, setAmount] = useState('');
  const [accountId, setAccountId] = useState('');
  const [accounts, setAccounts] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchAccounts();
  }, []);

  const fetchAccounts = async () => {
    try {
      const response = await getAccounts();
      setAccounts(response.data);
      if (response.data.length > 0) {
        setAccountId(response.data[0].id);
      }
    } catch (err) {
      setError('Failed to fetch accounts');
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    const amountNum = parseFloat(amount);
    
    if (description.trim() !== '' && !isNaN(amountNum) && accountId) {
      try {
        const newTransaction = {
          description,
          amount: amountNum,
          account: accountId,
          creator: 1, // Default user ID
          timestamp: new Date().toISOString()
        };
        
        await createTransaction(newTransaction);
        setDescription('');
        setAmount('');
        // Call the parent's callback to refresh the transaction list
        if (onTransactionCreated) {
          onTransactionCreated();
        }
      } catch (err) {
        setError('Failed to create transaction');
      }
    }
  };

  if (error) return <div className="error">{error}</div>;

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
            value={accountId}
            onChange={(e) => setAccountId(e.target.value)}
            required
          >
            {accounts.map((account) => (
              <option key={account.id} value={account.id}>
                {account.name}
              </option>
            ))}
          </select>
        </div>
        <button type="submit">Add Transaction</button>
      </form>
    </div>
  );
};

export default TransactionForm;
