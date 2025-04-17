import React, { useState, useEffect } from 'react';
import { getAccounts, deleteAccount as deleteAccountAPI } from '../services/api';

const AccountList = () => {
  const [accounts, setAccounts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchAccounts();
  }, []);

  const fetchAccounts = async () => {
    try {
      const response = await getAccounts();
      setAccounts(response.data);
      setLoading(false);
    } catch (err) {
      setError('Failed to fetch accounts');
      setLoading(false);
    }
  };

  const handleDeleteAccount = async (id) => {
    try {
      await deleteAccountAPI(id);
      setAccounts(accounts.filter(a => a.id !== id));
    } catch (err) {
      setError('Failed to delete account');
    }
  };

  if (loading) return <div>Loading accounts...</div>;
  if (error) return <div className="error">{error}</div>;

  return (
    <div className="account-list">
      <h2>Accounts</h2>
      {accounts.length === 0 ? (
        <p className="no-accounts">No accounts found.</p>
      ) : (
        <ul>
          {accounts.map((account) => (
            <li key={account.id}>
              <div className="account-info">
                <span className="name">{account.name}</span>
                <span className="owner">Owner: {account.owner.name}</span>
              </div>
              <button onClick={() => handleDeleteAccount(account.id)}>Delete</button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default AccountList; 