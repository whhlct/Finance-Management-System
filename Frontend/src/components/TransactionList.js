import React from 'react';

const TransactionList = ({ transactions, deleteTransaction }) => {
  return (
    <div className="transaction-list">
      <h2>Transaction History</h2>
      {transactions.length === 0 ? (
        <p>No transactions recorded.</p>
      ) : (
        <ul>
          {transactions.map((transaction) => (
            <li key={transaction.id}>
              <span className="description">{transaction.description}</span>
              <span className={`amount ${transaction.amount < 0 ? 'expense' : 'income'}`}>
                ${transaction.amount.toFixed(2)}
              </span>
              <button onClick={() => deleteTransaction(transaction.id)}>Delete</button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default TransactionList;
