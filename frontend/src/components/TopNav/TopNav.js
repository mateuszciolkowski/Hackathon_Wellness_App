import React from 'react';
import './TopNav.css';

function TopNav({ onLoginClick, onRegisterClick }) {
  return (
    <nav className="top-nav">
      <button 
        className="login-button" 
        onClick={onRegisterClick}
        style={{marginRight: '10px'}}
      >
        Zarejestruj się
      </button>
      <button className="login-button" onClick={onLoginClick}>
        Zaloguj się
      </button>
    </nav>
  );
}

export default TopNav;