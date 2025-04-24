import React from 'react';

const ReimbursementList = ({ reimbursements, updateReimbursementStatus }) => {
  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
  };

  // Function to handle status change
  const handleStatusChange = (id, newStatus) => {
    updateReimbursementStatus(id, newStatus);
  };

  return (
    <div className="reimbursement-list">
      <h2>Reimbursement Requests</h2>
      {reimbursements.length === 0 ? (
        <p className="no-reimbursements">No reimbursement requests found.</p>
      ) : (
        <div className="reimbursements-table">
          <table>
            <thead>
              <tr>
                <th>Date</th>
                <th>Name</th>
                <th>Description</th>
                <th>Category</th>
                <th>Amount</th>
                <th>Receipt</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {reimbursements.map((reimbursement) => (
                <tr key={reimbursement.id} className={`status-${reimbursement.status.toLowerCase()}`}>
                  <td>{formatDate(reimbursement.date)}</td>
                  <td>{reimbursement.name}</td>
                  <td className="description">{reimbursement.description}</td>
                  <td>{reimbursement.category}</td>
                  <td className="amount">${reimbursement.amount.toFixed(2)}</td>
                  <td>
                    {reimbursement.receipt !== 'No receipt attached' ? (
                      <a href="#" onClick={(e) => e.preventDefault()}>View Receipt</a>
                    ) : (
                      'No receipt'
                    )}
                  </td>
                  <td className={`status-${reimbursement.status.toLowerCase()}`}>
                    {reimbursement.status}
                  </td>
                  <td className="actions">
                    {reimbursement.status === 'Pending' && (
                      <>
                        <button 
                          className="approve-btn"
                          onClick={() => handleStatusChange(reimbursement.id, 'Approved')}
                        >
                          Approve
                        </button>
                        <button 
                          className="reject-btn"
                          onClick={() => handleStatusChange(reimbursement.id, 'Rejected')}
                        >
                          Reject
                        </button>
                      </>
                    )}
                    {reimbursement.status === 'Approved' && (
                      <button 
                        className="paid-btn"
                        onClick={() => handleStatusChange(reimbursement.id, 'Paid')}
                      >
                        Mark as Paid
                      </button>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default ReimbursementList; 