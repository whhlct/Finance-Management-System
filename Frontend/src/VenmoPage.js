import React from 'react';
import './VenmoPage.css';

function VenmoPage() {
    return (
        <div className="VenmoPage">
        <header className="hero">
            <div className="hero-content">
            <h1>Venmo</h1>
            <p>Effortlessly request reimbursment.</p>
            <button onClick={() => alert('Venmo Requested!')}>VenmoPage</button>
            </div>
        </header>
        </div>
    );
}