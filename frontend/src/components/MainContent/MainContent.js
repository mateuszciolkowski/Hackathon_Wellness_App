import React from 'react';
import './MainContent.css';
import Diary from '../Diary/Diary';
import User from '../User/User';

function MainContent({ activeComponent }) {
  const renderComponent = () => {
    switch (activeComponent) {
      case 'diary':
        return <div className="diary-section"><Diary /></div>;
      case 'user':
        return <div className="user-section"><User /></div>;
      case 'exercises':
        return (
          <div className="exercises-section">
            <h2>Ćwiczenia</h2>
            <p>Tutaj będzie zawartość sekcji ćwiczeń</p>
          </div>
        );
      default:
        return (
          <div className="welcome-section">
            <h1>Witaj w Twojej przestrzeni wellness</h1>
            <p>Zadbaj o swoje zdrowie psychiczne z naszymi narzędziami</p>
          </div>
        );
    }
  };

  return (
    <div className="main-content">
      {renderComponent()}
    </div>
  );
}

export default MainContent;