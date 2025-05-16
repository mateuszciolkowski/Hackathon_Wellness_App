import React from 'react';
import './Navbar.css';

function Navbar({ onComponentChange }) {
  return (
    <nav className="navbar">
      <button 
        className="nav-button home" 
        onClick={() => onComponentChange(null)}
      >
        Menu Główne
      </button>
      <div className="nav-icons">
        <button 
          className="nav-button pink" 
          onClick={() => onComponentChange('diary')}
        >
          Dziennik
        </button>
        <button 
          className="nav-button orange" 
          onClick={() => onComponentChange('meditation')}
        >
          Medytacja
        </button>
        <button 
          className="nav-button green" 
          onClick={() => onComponentChange('exercises')}
        >
          Ćwiczenia
        </button>
      </div>
    </nav>
  );
}

export default Navbar;