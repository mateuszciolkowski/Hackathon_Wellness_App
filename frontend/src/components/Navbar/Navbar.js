import React from 'react';
import './Navbar.css';

function Navbar() {
  return (
    <nav className="navbar">
      <div className="nav-icons">
        <button className="nav-button pink">Dziennik</button>
        <button className="nav-button orange">Medytacja</button>
        <button className="nav-button green">Ćwiczenia</button>
      </div>
    </nav>
  );
}

export default Navbar;