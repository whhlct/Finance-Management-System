import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 5000,
  withCredentials: true,
});

// Add response interceptor for better error handling
api.interceptors.response.use(
  (response) => {
    console.log('API Response:', response);
    return response;
  },
  (error) => {
    console.error('API Error:', error.response || error);
    if (error.response?.status === 404) {
      console.error('API endpoint not found');
    }
    return Promise.reject(error);
  }
);

// Add request interceptor for debugging
api.interceptors.request.use(
  (config) => {
    console.log('Making request to:', config.url);
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// User API calls
export const getUsers = () => api.get('/users/');
export const createUser = (userData) => api.post('/users/', userData);
export const updateUser = (id, userData) => api.put(`/users/${id}/`, userData);
export const deleteUser = (id) => api.delete(`/users/${id}/`);

// Account API calls
export const getAccounts = () => api.get('/accounts/');
export const createAccount = (accountData) => api.post('/accounts/', accountData);
export const updateAccount = (id, accountData) => api.put(`/accounts/${id}/`, accountData);
export const deleteAccount = (id) => api.delete(`/accounts/${id}/`);

// Transaction API calls
export const getTransactions = () => api.get('/transactions/');
export const createTransaction = (transactionData) => api.post('/transactions/', transactionData);
export const updateTransaction = (id, transactionData) => api.put(`/transactions/${id}/`, transactionData);
export const deleteTransaction = (id) => api.delete(`/transactions/${id}/`);

export default api; 