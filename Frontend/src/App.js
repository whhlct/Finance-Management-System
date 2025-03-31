import React, { useState } from 'react';
import Hero from './components/hero';
import BudgetControl from './components/BudgetControl';
import TransactionForm from './components/TransactionForm';
import TransactionList from './components/TransactionList';
import './App.css';

function App() {
  // Define budget categories
  const budgetCategories = [
    'Recruitment',
    'Brotherhood',
    'Alumni',
    'Health and Safety',
    'General'
  ];

  // State for each budget category
  const [budgets, setBudgets] = useState({
    Recruitment: 200,
    Brotherhood: 200,
    Alumni: 200,
    'Health and Safety': 200,
    General: 200
  });
  
  const [transactions, setTransactions] = useState([]);

  // Calculate total budget
  const totalBudget = Object.values(budgets).reduce((sum, amount) => sum + amount, 0);

  // When a transaction is added, update the transaction history and adjust the budget.
  const addTransaction = (transaction) => {
    setTransactions([transaction, ...transactions]);
    
    // Update the specific budget category
    setBudgets({
      ...budgets,
      [transaction.category]: budgets[transaction.category] + transaction.amount
    });
  };

  // Delete a transaction and revert its effect on the budget.
  const deleteTransaction = (id) => {
    const transactionToDelete = transactions.find((t) => t.id === id);
    if (transactionToDelete) {
      setBudgets({
        ...budgets,
        [transactionToDelete.category]: budgets[transactionToDelete.category] - transactionToDelete.amount
      });
    }
    setTransactions(transactions.filter((t) => t.id !== id));
  };

  // Function for direct budget adjustment (from BudgetControl)
  const adjustBudget = (category, amount) => {
    setBudgets({
      ...budgets,
      [category]: budgets[category] + amount
    });
  };

  return (
    <div className="App">
      <Hero />
      <main className="main-content">
        <section className="controls">
          <BudgetControl 
            budgets={budgets} 
            totalBudget={totalBudget} 
            adjustBudget={adjustBudget} 
            categories={budgetCategories} 
          />
        </section>
        <section className="transactions">
          <TransactionForm 
            addTransaction={addTransaction} 
            categories={budgetCategories} 
          />
          <TransactionList 
            transactions={transactions} 
            deleteTransaction={deleteTransaction} 
          />
        </section>
      </main>
    </div>
  );
}

export default App;
