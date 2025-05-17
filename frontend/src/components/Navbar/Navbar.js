import React from 'react';
import './Navbar.css';

function Navbar({ onComponentChange }) {
  const handleChartClick = () => {
    onComponentChange('chart');
  };

  return (
    <nav className="navbar">
      <div className="nav-buttons">
        <button 
          className="nav-button home" 
          onClick={() => onComponentChange(null)}
        >
          Codzienne Pytania
        </button>
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
          className="nav-button blue"
          onClick={() => onComponentChange('aiHandler')}
        >
          AI Asystent
        </button>
        <button 
          className="nav-button purple" 
          onClick={handleChartClick}
        >
          Statystyki
        </button>
      </div>
    </nav>
  );
}

export default Navbar;