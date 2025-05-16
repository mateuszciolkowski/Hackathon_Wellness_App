import React from 'react';
import './HomePage.css';

function HomePage() {
  return (
    <div className="home-page">
      <div className="welcome-content">
        <h1>Witaj w aplikacji Wellness</h1>
        <p>Twoje miejsce do dbania o zdrowie psychiczne</p>
        <div className="features">
          <div className="feature pink">
            <h3>Dziennik</h3>
            <p>Zapisuj swoje myśli i emocje</p>
          </div>
          <div className="feature orange">
            <h3>Medytacja</h3>
            <p>Ćwiczenia mindfulness</p>
          </div>
          <div className="feature green">
            <h3>Ćwiczenia</h3>
            <p>Aktywności wspierające dobre samopoczucie</p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default HomePage;