import React, { useState } from 'react';
import Hero from './components/hero';
import TransactionForm from './components/TransactionForm';
import TransactionList from './components/TransactionList';
import AccountForm from './components/AccountForm';
import AccountList from './components/AccountList';
import './App.css';

function App() {
  const [refreshAccounts, setRefreshAccounts] = useState(0);
  const [refreshTransactions, setRefreshTransactions] = useState(0);

  const handleAccountCreated = () => {
    setRefreshAccounts(prev => prev + 1);
  };

  const handleTransactionCreated = () => {
    setRefreshTransactions(prev => prev + 1);
  };

  return (
    <div className="App">
      <Hero />
      <main className="main-content">
        <div className="accounts-section">
          <AccountForm onAccountCreated={handleAccountCreated} />
          <AccountList key={refreshAccounts} />
        </div>
        
        <section className="transactions">
          <TransactionForm onTransactionCreated={handleTransactionCreated} />
          <TransactionList key={refreshTransactions} />
        </section>
      </main>
    </div>
  );
}

export default App;
