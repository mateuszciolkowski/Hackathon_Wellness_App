import React from 'react';
import './History.css';

function History() {
  // Przykładowe dane wpisów (w przyszłości do zastąpienia danymi z API/bazy danych)
  const entries = [
    {
      id: 1,
      date: "2024-01-15",
      content: "Dzisiaj był wspaniały dzień. Udało mi się zrealizować wszystkie zaplanowane zadania i znalazłem chwilę na relaks.",
      mood: "😊"
    },
    {
      id: 2,
      date: "2024-01-14",
      content: "Trudny dzień w pracy, ale medytacja pomogła mi się zrelaksować i zachować spokój.",
      mood: "😌"
    },
    {
      id: 3,
      date: "2024-01-13",
      content: "Spędziłem miło czas z rodziną. Takie chwile są bezcenne dla mojego samopoczucia.",
      mood: "🥰"
    }
  ];

  return (
    <div className="history-container">
      <div className="history-header">
        <h2>Moje Wpisy</h2>
        <p>Historia Twoich przemyśleń i doświadczeń</p>
      </div>
      
      <div className="entries-timeline">
        {entries.map(entry => (
          <div key={entry.id} className="entry-card">
            <div className="entry-date">
              <span className="date-day">{new Date(entry.date).getDate()}</span>
              <span className="date-month">{new Date(entry.date).toLocaleString('pl-PL', { month: 'short' })}</span>
            </div>
            <div className="entry-content">
              <div className="entry-mood">{entry.mood}</div>
              <p>{entry.content}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default History;