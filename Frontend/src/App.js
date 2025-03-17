import React from 'react';
import Hero from './Components/hero';
import BudgetControl from './Components/budgetcontrol';
import InventoryControl from './Components/InventoryControl';
import './App.css';

function App() {
  return (
    <div className="App">
      <Hero />
      <main className="main-content">
        <BudgetControl />
        <InventoryControl />
      </main>
    </div>
  );
}

export default App;
