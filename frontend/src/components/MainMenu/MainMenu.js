import React from 'react';
import './MainMenu.css';

function MainMenu() {
  return (
    <nav className="main-menu">
      <button className="menu-button pink">Dziennik</button>
      <button className="menu-button orange">Medytacja</button>
      <button className="menu-button green">Ćwiczenia</button>
    </nav>
  );
}

export default MainMenu;