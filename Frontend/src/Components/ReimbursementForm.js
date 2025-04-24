import React, { useState } from 'react';

const ReimbursementForm = ({ categories, addReimbursement }) => {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [amount, setAmount] = useState('');
  const [description, setDescription] = useState('');
  const [category, setCategory] = useState(categories[0]);
  const [receipt, setReceipt] = useState(null);
  const [status, setStatus] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    
    const amountNum = parseFloat(amount);
    
    if (name.trim() !== '' && email.trim() !== '' && description.trim() !== '' && !isNaN(amountNum)) {
      const newReimbursement = {
        id: Math.floor(Math.random() * 1000000),
        name,
        email,
        description,
        amount: amountNum,
        category,
        receipt: receipt ? receipt.name : 'No receipt attached',
        date: new Date().toISOString(),
        status: 'Pending'
      };
      
      addReimbursement(newReimbursement);
      setStatus('Reimbursement request submitted successfully!');
      
      // Reset form
      setName('');
      setEmail('');
      setAmount('');
      setDescription('');
      setCategory(categories[0]);
      setReceipt(null);
      
      // Clear success message after 3 seconds
      setTimeout(() => {
        setStatus('');
      }, 3000);
    } else {
      setStatus('Please fill in all required fields');
    }
  };

  const handleFileChange = (e) => {
    if (e.target.files.length > 0) {
      setReceipt(e.target.files[0]);
    }
  };

  return (
    <div className="reimbursement-form">
      <h2>Submit Reimbursement Request</h2>
      {status && <div className={status.includes('successfully') ? 'success-message' : 'error-message'}>{status}</div>}
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="name">Full Name</label>
          <input
            id="name"
            type="text"
            placeholder="Your Name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
          />
        </div>
        <div className="form-group">
          <label htmlFor="email">Email Address</label>
          <input
            id="email"
            type="email"
            placeholder="Your Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>
        <div className="form-group">
          <label htmlFor="amount">Amount ($)</label>
          <input
            id="amount"
            type="number"
            step="0.01"
            placeholder="Amount in dollars"
            value={amount}
            onChange={(e) => setAmount(e.target.value)}
            required
          />
        </div>
        <div className="form-group">
          <label htmlFor="category">Budget Category</label>
          <select 
            id="category"
            value={category} 
            onChange={(e) => setCategory(e.target.value)}
            className="category"
          >
            {categories.map((cat) => (
              <option key={cat} value={cat}>{cat}</option>
            ))}
          </select>
        </div>
        <div className="form-group">
          <label htmlFor="description">Description</label>
          <textarea
            id="description"
            placeholder="Detailed description of expenses"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            required
          />
        </div>
        <div className="form-group">
          <label htmlFor="receipt">Upload Receipt (optional)</label>
          <input
            id="receipt"
            type="file"
            accept="image/*,.pdf"
            onChange={handleFileChange}
          />
          {receipt && <p className="file-selected">File selected: {receipt.name}</p>}
        </div>
        <button type="submit" className="submit-btn">Submit Reimbursement Request</button>
      </form>
    </div>
  );
};

export default ReimbursementForm; 