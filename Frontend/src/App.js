import React, { useState } from 'react';
import Hero from './Components/hero';
import TransactionForm from './Components/TransactionForm';
import TransactionList from './Components/TransactionList';
import BudgetControl from './Components/BudgetControl';
import InventoryControl from './Components/InventoryControl';
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
  const [activeCategory, setActiveCategory] = useState('all');

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

  // Function for direct budget adjustment
  const adjustBudget = (category, amount) => {
    setBudgets({
      ...budgets,
      [category]: budgets[category] + amount
    });
  };

  // Filter transactions by category if a specific one is selected
  const filteredTransactions = activeCategory === 'all' 
    ? transactions 
    : transactions.filter(t => t.category === activeCategory);

  return (
    <div className="App">
      <Hero totalBudget={totalBudget} categoriesCount={budgetCategories.length} />
      <main className="main-content">
        <div className="budget-overview">
          <h2>Total Budget: ${totalBudget.toFixed(2)}</h2>
          <div className="budget-tabs">
            <button 
              className={activeCategory === 'all' ? 'active' : ''} 
              onClick={() => setActiveCategory('all')}
            >
              All Categories
            </button>
            {budgetCategories.map(category => (
              <button 
                key={category}
                className={activeCategory === category ? 'active' : ''}
                onClick={() => setActiveCategory(category)}
              >
                {category}
              </button>
            ))}
          </div>
        </div>

        <div className="budget-details">
          {activeCategory === 'all' ? (
            <div className="budget-cards">
              {budgetCategories.map(category => (
                <div key={category} className="budget-card">
                  <h3>{category}</h3>
                  <p className="budget-amount">${budgets[category].toFixed(2)}</p>
                  <div className="budget-controls">
                    <button onClick={() => adjustBudget(category, -50)}>-$50</button>
                    <button onClick={() => adjustBudget(category, 50)}>+$50</button>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="single-budget">
              <h3>{activeCategory} Budget</h3>
              <p className="budget-amount">${budgets[activeCategory].toFixed(2)}</p>
              <div className="budget-adjustment">
                <input 
                  type="number" 
                  placeholder="Enter amount" 
                  id="budgetAmount" 
                />
                <button onClick={() => {
                  const amount = parseFloat(document.getElementById('budgetAmount').value);
                  if (!isNaN(amount)) {
                    adjustBudget(activeCategory, amount);
                    document.getElementById('budgetAmount').value = '';
                  }
                }}>
                  Adjust Budget
                </button>
              </div>
              <div className="budget-quickactions">
                <button onClick={() => adjustBudget(activeCategory, -100)}>-$100</button>
                <button onClick={() => adjustBudget(activeCategory, -50)}>-$50</button>
                <button onClick={() => adjustBudget(activeCategory, 50)}>+$50</button>
                <button onClick={() => adjustBudget(activeCategory, 100)}>+$100</button>
              </div>
            </div>
          )}
        </div>

        <section className="transactions">
          <TransactionForm 
            addTransaction={addTransaction} 
            categories={budgetCategories} 
            defaultCategory={activeCategory !== 'all' ? activeCategory : budgetCategories[0]}
          />
          <TransactionList 
            transactions={filteredTransactions} 
            deleteTransaction={deleteTransaction} 
            title={activeCategory === 'all' ? 'All Transactions' : `${activeCategory} Transactions`}
          />
        </section>
      </main>
    </div>
  );
}

export default App;
