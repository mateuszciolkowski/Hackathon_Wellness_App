import React from 'react';
import './TopNav.css';

function TopNav({ onLoginClick }) {
  return (
    <nav className="top-nav">
      <button className="login-button" onClick={onLoginClick}>
        Zaloguj się
      </button>
    </nav>
  );
}

export default TopNav;