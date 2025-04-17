# Front End

A React frontend application to help fraternity chapters manage their financial resources efficiently. **This documentation covers only the frontend implementation**—backend services, APIs, and data persistence are out of scope.

---

## Table of Contents

1. [Introduction](#introduction)  
2. [Technology Stack](#technology-stack)  
3. [Project Structure](#project-structure)  
4. [Component Documentation](#component-documentation)  
5. [UI Elements](#ui-elements)  
6. [Styling](#styling)  
7. [Getting Started](#getting-started)  
8. [Available Scripts](#available-scripts)  
9. [Learn More](#learn-more)  
10. [Code Splitting](#code-splitting)  
11. [Analyzing Bundle Size](#analyzing-bundle-size)  
12. [Making a Progressive Web App](#making-a-progressive-web-app)  
13. [Advanced Configuration](#advanced-configuration)  
14. [Deployment](#deployment)  
15. [Troubleshooting](#troubleshooting)

---

## Introduction

**Frontend Only**—this README describes the React-based UI. All state is managed client‑side; integration with backend APIs or databases is not covered here.

Fraternity Finance Tracker enables chapters to:

- Define and adjust category budgets  
- Log income and expenses  
- View transaction history with filtering and deletion  
- Apply preset budget templates  
- Track simple inventory counts  

---

## Technology Stack

- **Framework:** React.js (Create React App)  
- **Styling:** Custom CSS  
- **State Management:** React Hooks (`useState`, `useEffect`)  

---

## Project Structure

```
src/
├── components/
│   ├── Hero.js
│   ├── BudgetControl.js
│   ├── TransactionForm.js
│   ├── TransactionList.js
│   └── InventoryControl.js
├── data/
│   ├── budgetTemplates.json
│   └── transactionTemplates.json
├── App.css
├── App.js
└── index.js
```

---

## Component Documentation

### App.js  
**Purpose:** Main container orchestrating state and data flow.  
- **State Variables:**  
  - `budgets`: object mapping categories to amounts  
  - `transactions`: array of transaction objects  
  - `activeCategory`: currently filtered category  
  - `customIncrement`: value for manual budget adjustments  
  - `selectedBudgetPreset`: name of applied preset  
- **Key Functions:**  
  - `calculateTotalBudget()`  
  - `addTransaction()` / `deleteTransaction()`  
  - `adjustBudget(category, amount)`  
  - `applyPreset(presetName)`  

### Hero.js  
**Purpose:** Landing section with title and key stats.  
- **Props:**  
  - `totalBudget` (number)  
  - `categoriesCount` (number)  
  - `brotherhoodSize` (number)  
- **Displays:**  
  - App title and description  
  - “Budget Categories”, “Total Budget”, “Brotherhood Size” stats  
  - Navigation buttons to Budget and Transactions sections  

### BudgetControl.js  
**Purpose:** Interface for adjusting category budgets.  
- **Props:**  
  - `budgets` (object)  
  - `totalBudget` (number)  
  - `adjustBudget` (fn)  
  - `categories` (array)  
- **Features:**  
  - Quick +/– buttons per category  
  - Custom increment input with “Apply” button  

### TransactionForm.js  
**Purpose:** Form for adding new financial transactions.  
- **Props:**  
  - `addTransaction` (fn)  
  - `categories` (array)  
  - `defaultCategory?` (string)  
- **State Variables:**  
  - `description` (string)  
  - `amount` (number)  
  - `category` (string)  
- **Functionality:**  
  - Input validation (required fields, numeric amount)  
  - Constructs transaction object with timestamp  

### TransactionList.js  
**Purpose:** Displays transaction history.  
- **Props:**  
  - `transactions` (array)  
  - `deleteTransaction` (fn)  
  - `title?` (string)  
- **Features:**  
  - Formats dates (e.g., “Apr 17, 2025”)  
  - Color‑codes amounts (green for income, red for expense)  
  - Delete button per entry  

### InventoryControl.js  
**Purpose:** Simple inventory tracking.  
- **State Variables:**  
  - `inventory` (number)  
- **Features:**  
  - Increment/decrement buttons  
  - Displays current count  

---

## UI Elements

- **Budget Cards:**  
  - Category name  
  - Current amount  
  - ± buttons  
  - Custom adjust input  

- **Transaction Entry Form:**  
  - Fields for description, amount, category  
  - Submit button with disabled state until valid  

- **Transaction History List:**  
  - Scrollable container  
  - Date, description, category labels  
  - Color-coded amount and delete icon  

- **Budget Controls:**  
  - Category filter tabs  
  - Preset selector dropdown + “Apply Preset” button  
  - Quick increment/decrement action buttons  

---

## Styling

- Responsive design (mobile to desktop)  
- Card-based layout with soft shadows  
- Color coding:  
  - Green for incomes  
  - Red for expenses  
- Hover/focus states on buttons and inputs  
- Consistent typography and spacing  

---

## Getting Started

This project was bootstrapped with [Create React App](https://github.com/facebook/create-react-app).

1. **Install dependencies**  
   ```bash
   npm install
   ```
2. **Run in development mode**  
   ```bash
   npm start
   ```
   Opens [http://localhost:3000](http://localhost:3000) in your browser.  
3. **Build for production**  
   ```bash
   npm run build
   ```
   Bundled files output to `build/`.  

---

## Available Scripts

In the project directory, you can run:

- **`npm start`**  
  Starts the development server with hot reloading.

- **`npm test`**  
  Launches the test runner in interactive watch mode.

- **`npm run build`**  
  Bundles React for production, outputs optimized files to `build/`.

- **`npm run eject`**  
  **One‑way operation!** Exposes build configs for customization.  

---

## Learn More

- **Create React App Documentation:**  
  https://facebook.github.io/create-react-app/docs/getting-started

- **React Documentation:**  
  https://reactjs.org/

---

## Code Splitting

Moved to:  
https://facebook.github.io/create-react-app/docs/code-splitting

---

## Analyzing Bundle Size

Moved to:  
https://facebook.github.io/create-react-app/docs/analyzing-the-bundle-size

---

## Making a Progressive Web App

Moved to:  
https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app

---

## Advanced Configuration

Moved to:  
https://facebook.github.io/create-react-app/docs/advanced-configuration

---

## Deployment

Moved to:  
https://facebook.github.io/create-react-app/docs/deployment

---

## Troubleshooting

If `npm run build` fails to minify, see:  
https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify