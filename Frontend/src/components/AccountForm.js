import React, { useState, useEffect } from 'react';
import { createAccount } from '../services/api';
import { getUsers } from '../services/api';

const AccountForm = ({ onAccountCreated }) => {
  const [name, setName] = useState('');
  const [ownerId, setOwnerId] = useState('');
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchUsers();
  }, []);

  const fetchUsers = async () => {
    try {
      const response = await getUsers();
      setUsers(response.data);
      if (response.data.length > 0) {
        setOwnerId(response.data[0].id);
      }
      setLoading(false);
    } catch (err) {
      setError('Failed to fetch users');
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (name.trim() !== '' && ownerId) {
      try {
        const newAccount = {
          name,
          owner: ownerId
        };
        
        await createAccount(newAccount);
        setName('');
        // Call the parent's callback to refresh the account list
        if (onAccountCreated) {
          onAccountCreated();
        }
      } catch (err) {
        setError('Failed to create account');
      }
    }
  };

  if (loading) return <div>Loading users...</div>;
  if (error) return <div className="error">{error}</div>;

  return (
    <div className="account-form">
      <h2>Add New Account</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <input
            type="text"
            placeholder="Account Name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
          />
        </div>
        <div className="form-group">
          <select 
            value={ownerId} 
            onChange={(e) => setOwnerId(e.target.value)}
            className="owner"
            required
          >
            {users.map((user) => (
              <option key={user.id} value={user.id}>{user.name}</option>
            ))}
          </select>
        </div>
        <button type="submit">Add Account</button>
      </form>
    </div>
  );
};

export default AccountForm; 