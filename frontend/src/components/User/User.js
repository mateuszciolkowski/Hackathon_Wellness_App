import React from 'react';
import './User.css';

function User() {
  // Przykładowe dane użytkownika (w przyszłości można zastąpić danymi z API/bazy danych)
  const userData = {
    imie: "Jan",
    nazwisko: "Kowalski",
    email: "jan.kowalski@example.com",
    dataRejestracji: "01.01.2024"
  };

  const handleGenerateReport = () => {
    // Tutaj w przyszłości będzie logika generowania raportu
    console.log("Generowanie raportu...");
  };

  return (
    <div className="user-container">
      <div className="user-header">
        <h2>Profil Użytkownika</h2>
      </div>
      
      <div className="user-info">
        <div className="info-group">
          <label>Imię:</label>
          <span>{userData.imie}</span>
        </div>
        <div className="info-group">
          <label>Nazwisko:</label>
          <span>{userData.nazwisko}</span>
        </div>
        <div className="info-group">
          <label>Email:</label>
          <span>{userData.email}</span>
        </div>
        <div className="info-group">
          <label>Data rejestracji:</label>
          <span>{userData.dataRejestracji}</span>
        </div>
      </div>

      <div className="user-actions">
        <button 
          className="report-button"
          onClick={handleGenerateReport}
        >
          Generuj Raport Aktywności
        </button>
      </div>
    </div>
  );
}

export default User;