import React from 'react';

const TransactionList = ({ transactions, deleteTransaction, title = 'Transaction History' }) => {
  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
  };

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
                {transaction.date && <span className="date">{formatDate(transaction.date)}</span>}
                <span className="category">{transaction.category}</span>
                <span className={`amount ${transaction.amount >= 0 ? 'income' : 'expense'}`}>
                  {transaction.amount >= 0 ? '+' : ''}${Math.abs(transaction.amount).toFixed(2)}
                </span>
              </div>
              <button onClick={() => deleteTransaction(transaction.id)}>Delete</button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default TransactionList;
