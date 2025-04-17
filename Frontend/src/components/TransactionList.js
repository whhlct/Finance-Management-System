import React, { useEffect, useState } from 'react';
import { getTransactions, deleteTransaction as deleteTransactionAPI } from '../services/api';

const TransactionList = ({ title = 'Transaction History' }) => {
  const [transactions, setTransactions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchTransactions();
  }, []);

  const fetchTransactions = async () => {
    try {
      const response = await getTransactions();
      setTransactions(response.data);
      setLoading(false);
    } catch (err) {
      setError('Failed to fetch transactions');
      setLoading(false);
    }
  };

  const handleDeleteTransaction = async (id) => {
    try {
      await deleteTransactionAPI(id);
      setTransactions(transactions.filter(t => t.id !== id));
    } catch (err) {
      setError('Failed to delete transaction');
    }
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
  };

  if (loading) return <div>Loading transactions...</div>;
  if (error) return <div className="error">{error}</div>;

  return (
    <div className="transaction-list">
      <h2>{title}</h2>
      {transactions.length === 0 ? (
        <p className="no-transactions">No transactions found.</p>
      ) : (
        <ul>
          {transactions.map((transaction) => (
            <li key={transaction.id}>
              <div className="transaction-info">
                <span className="description">{transaction.description}</span>
                {transaction.timestamp && <span className="date">{formatDate(transaction.timestamp)}</span>}
                <span className="account">{transaction.account.name}</span>
                <span className={`amount ${transaction.amount >= 0 ? 'income' : 'expense'}`}>
                  {transaction.amount >= 0 ? '+' : ''}${Math.abs(transaction.amount).toFixed(2)}
                </span>
              </div>
              <button onClick={() => handleDeleteTransaction(transaction.id)}>Delete</button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default TransactionList;
