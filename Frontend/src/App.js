import React, { useState, useEffect } from 'react';
import Hero from './components/hero';
import TransactionForm from './components/TransactionForm';
import TransactionList from './components/TransactionList';
import ReimbursementForm from './components/ReimbursementForm';
import ReimbursementList from './components/ReimbursementList';
import './App.css';

// Import template data
import budgetTemplatesData from './data/budgetTemplates.json';
import transactionTemplatesData from './data/transactionTemplates.json';

function App() {
  // Define budget categories
  const budgetCategories = [
    'Recruitment',
    'Brotherhood',
    'Alumni',
    'Health and Safety',
    'New Member',
    'Philanthropy',
    'Marketing',
    'Housing'
  ];

  // State for each budget category
  const [budgets, setBudgets] = useState(budgetTemplatesData.defaultBudgets);
  
  const [transactions, setTransactions] = useState([]);
  const [reimbursements, setReimbursements] = useState([]);
  const [activeCategory, setActiveCategory] = useState('all');
  const [activeTab, setActiveTab] = useState('budget'); // 'budget', 'transactions', 'reimbursements'
  const [budgetInputs, setBudgetInputs] = useState(
    Object.fromEntries(
      budgetCategories.map(category => [
        category, 
        { amount: '', description: '' }
      ])
    )
  );
  const [selectedBudgetPreset, setSelectedBudgetPreset] = useState('total');

  // Load template transactions
  useEffect(() => {
    setTransactions(transactionTemplatesData.transactions);
  }, []);

  // Calculate total budget
  const totalBudget = Object.values(budgets).reduce((sum, amount) => sum + amount, 0);

  // When a transaction is added, update the transaction history and adjust the budget.
  const addTransaction = (transaction) => {
    // Generate a new unique ID based on the highest existing ID
    const highestId = transactions.length > 0 
      ? Math.max(...transactions.map(t => t.id)) 
      : 0;
      
    const newTransaction = {
      ...transaction,
      id: highestId + 1
    };

    setTransactions([newTransaction, ...transactions]);
    
    // Update the specific budget category
    setBudgets({
      ...budgets,
      [transaction.category]: budgets[transaction.category] + transaction.amount
    });
  };

  // Add a reimbursement request
  const addReimbursement = (reimbursement) => {
    const highestId = reimbursements.length > 0 
      ? Math.max(...reimbursements.map(r => r.id)) 
      : 0;
      
    const newReimbursement = {
      ...reimbursement,
      id: highestId + 1
    };

    setReimbursements([newReimbursement, ...reimbursements]);
  };

  // Update reimbursement status
  const updateReimbursementStatus = (id, newStatus) => {
    setReimbursements(
      reimbursements.map(reimbursement => 
        reimbursement.id === id 
          ? { ...reimbursement, status: newStatus } 
          : reimbursement
      )
    );

    // If approved, add negative transaction (expense) to the budget
    if (newStatus === 'Approved') {
      const approvedReimbursement = reimbursements.find(r => r.id === id);
      if (approvedReimbursement) {
        const reimbursementTransaction = {
          id: Math.floor(Math.random() * 1000000),
          description: `Reimbursement: ${approvedReimbursement.description} (${approvedReimbursement.name})`,
          amount: -approvedReimbursement.amount, // Negative amount as it's an expense
          category: approvedReimbursement.category,
          date: new Date().toISOString()
        };
        
        addTransaction(reimbursementTransaction);
      }
    }
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

  // Function for direct budget adjustment with custom amount
  const adjustBudget = (category, amount) => {
    const newAmount = budgets[category] + amount;
    // Prevent negative budgets, minimum is zero
    setBudgets({
      ...budgets,
      [category]: newAmount >= 0 ? newAmount : 0
    });
  };

  // Update input for a specific category
  const updateBudgetInput = (category, field, value) => {
    setBudgetInputs({
      ...budgetInputs,
      [category]: {
        ...budgetInputs[category],
        [field]: value
      }
    });
  };

  // Apply budget adjustment and clear inputs
  const applyBudgetAdjustment = (category, isIncrease) => {
    const amount = parseFloat(budgetInputs[category].amount);
    if (!isNaN(amount)) {
      adjustBudget(category, isIncrease ? amount : -amount);
      // Clear inputs for this category only
      updateBudgetInput(category, 'amount', '');
      updateBudgetInput(category, 'description', '');
    }
  };

  // Function to apply a budget preset
  const applyBudgetPreset = (presetName) => {
    const preset = budgetTemplatesData.budgetPresets.find(p => p.name === presetName);
    if (preset) {
      setBudgets(preset.budgets);
    }
  };

  // Filter transactions by category if a specific one is selected
  const filteredTransactions = activeCategory === 'all' 
    ? transactions 
    : transactions.filter(t => t.category === activeCategory);

  return (
    <div className="App">
      <Hero totalBudget={totalBudget} categoriesCount={budgetCategories.length} />
      <main className="main-content">
        <div className="main-tabs">
          <button 
            className={activeTab === 'budget' ? 'active' : ''} 
            onClick={() => setActiveTab('budget')}
          >
            Budget Management
          </button>
          <button 
            className={activeTab === 'transactions' ? 'active' : ''} 
            onClick={() => setActiveTab('transactions')}
          >
            Transactions
          </button>
          <button 
            className={activeTab === 'reimbursements' ? 'active' : ''} 
            onClick={() => setActiveTab('reimbursements')}
          >
            Reimbursements
          </button>
        </div>

        {activeTab === 'budget' && (
          <>
            <div className="budget-overview">
              <h2>Total Budget: ${totalBudget.toFixed(2)}</h2>
              
              <div className="budget-presets">
                <h3>Budget Presets</h3>
                <div className="preset-selector">
                  <select 
                    value={selectedBudgetPreset} 
                    onChange={(e) => setSelectedBudgetPreset(e.target.value)}
                  >
                    <option value="total">Total Budget</option>
                    {budgetTemplatesData.budgetPresets.map((preset, index) => (
                      <option key={index} value={preset.name}>{preset.name}</option>
                    ))}
                  </select>
                  <button 
                    onClick={() => {
                      if (selectedBudgetPreset === 'total') {
                        // Reset to original total budget
                        setBudgets(budgetTemplatesData.defaultBudgets);
                      } else if (selectedBudgetPreset) {
                        applyBudgetPreset(selectedBudgetPreset);
                      }
                    }}
                  >
                    Apply
                  </button>
                </div>
              </div>
              
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
                      <div className="budget-adjustment">
                        <input
                          type="number"
                          placeholder="Enter amount"
                          value={budgetInputs[category].amount}
                          onChange={(e) => updateBudgetInput(category, 'amount', e.target.value)}
                        />
                        <input
                          type="text"
                          placeholder="Description"
                          value={budgetInputs[category].description}
                          onChange={(e) => updateBudgetInput(category, 'description', e.target.value)}
                        />
                        <div className="budget-buttons">
                          <button 
                            onClick={() => applyBudgetAdjustment(category, false)}
                            disabled={!budgetInputs[category].amount}
                            className="decrease-btn"
                          >
                            Decrease
                          </button>
                          <button 
                            onClick={() => applyBudgetAdjustment(category, true)}
                            disabled={!budgetInputs[category].amount}
                            className="increase-btn"
                          >
                            Increase
                          </button>
                        </div>
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
                      value={budgetInputs[activeCategory].amount}
                      onChange={(e) => updateBudgetInput(activeCategory, 'amount', e.target.value)}
                    />
                    <input 
                      type="text" 
                      placeholder="Description" 
                      value={budgetInputs[activeCategory].description}
                      onChange={(e) => updateBudgetInput(activeCategory, 'description', e.target.value)}
                    />
                    <div className="budget-buttons">
                      <button 
                        onClick={() => applyBudgetAdjustment(activeCategory, false)}
                        disabled={!budgetInputs[activeCategory].amount}
                        className="decrease-btn"
                      >
                        Decrease
                      </button>
                      <button 
                        onClick={() => applyBudgetAdjustment(activeCategory, true)}
                        disabled={!budgetInputs[activeCategory].amount}
                        className="increase-btn"
                      >
                        Increase
                      </button>
                    </div>
                  </div>
                </div>
              )}
            </div>
          </>
        )}

        {activeTab === 'transactions' && (
          <div className="transactions-section">
            <div className="transactions-container">
              <TransactionForm 
                addTransaction={addTransaction} 
                categories={budgetCategories}
                defaultCategory={activeCategory !== 'all' ? activeCategory : undefined}
              />
              <TransactionList 
                transactions={filteredTransactions} 
                deleteTransaction={deleteTransaction}
              />
            </div>
          </div>
        )}

        {activeTab === 'reimbursements' && (
          <div className="reimbursements-section">
            <div className="reimbursements-container">
              <ReimbursementForm 
                categories={budgetCategories}
                addReimbursement={addReimbursement}
              />
              <ReimbursementList 
                reimbursements={reimbursements}
                updateReimbursementStatus={updateReimbursementStatus}
              />
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
