import React from 'react';
import './Navbar.css';

function Navbar({ onComponentChange }) {
  const handleChartClick = () => {
    // Najpierw zmieniamy aktywny komponent na 'chart'
    onComponentChange('chart');
  };

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
          Nowy wpis
        </button>
        <button 
          className="nav-button orange" 
          onClick={() => onComponentChange('user')}
        >
          Użytkownik
        </button>
        <button 
          className="nav-button green" 
          onClick={() => onComponentChange('history')}
        >
          Moje wpisy
        </button>
        <button 
          className="nav-button blue" alt="AI"
          onClick={() => onComponentChange('aiHandler')}
        >
          AI Obsługa
        </button>
        <button 
          className="nav-button purple" 
          onClick={handleChartClick}
        >
          Wykresy
        </button>
      </div>
    </nav>
  );
}

export default Navbar;