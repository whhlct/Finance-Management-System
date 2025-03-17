import React, { useState } from 'react';
import Hero from './components/Hero';
import BudgetControl from './components/BudgetControl';
import InventoryControl from './components/InventoryControl';
import TransactionForm from './components/TransactionForm';
import TransactionList from './components/TransactionList';
import './App.css';

function App() {
  const [budget, setBudget] = useState(1000);
  const [inventory, setInventory] = useState(50);
  const [transactions, setTransactions] = useState([]);

  // When a transaction is added, update the transaction history and adjust the budget.
  const addTransaction = (transaction) => {
    setTransactions([transaction, ...transactions]);
    setBudget(budget + transaction.amount);
  };

  // Delete a transaction and revert its effect on the budget.
  const deleteTransaction = (id) => {
    const transactionToDelete = transactions.find((t) => t.id === id);
    if (transactionToDelete) {
      setBudget(budget - transactionToDelete.amount);
    }
    setTransactions(transactions.filter((t) => t.id !== id));
  };

  // Function for direct budget adjustment (from BudgetControl)
  const adjustBudget = (amount) => {
    setBudget(budget + amount);
  };

  // Function for inventory adjustments (from InventoryControl)
  const adjustInventory = (amount) => {
    setInventory(inventory + amount);
  };

  return (
    <div className="App">
      <Hero />
      <main className="main-content">
        <section className="controls">
          <BudgetControl budget={budget} adjustBudget={adjustBudget} />
          <InventoryControl inventory={inventory} adjustInventory={adjustInventory} />
        </section>
        <section className="transactions">
          <TransactionForm addTransaction={addTransaction} />
          <TransactionList transactions={transactions} deleteTransaction={deleteTransaction} />
        </section>
      </main>
    </div>
  );
}

export default App;
