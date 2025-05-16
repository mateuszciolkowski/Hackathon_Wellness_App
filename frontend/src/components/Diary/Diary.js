import React, { useState } from 'react';
import './Diary.css';

function Diary() {
  const [entries, setEntries] = useState([]);
  const [newEntry, setNewEntry] = useState('');

  const handleAddEntry = (e) => {
    e.preventDefault();
    if (newEntry.trim() !== '') {
      const entry = {
        id: Date.now(),
        text: newEntry,
        date: new Date().toLocaleDateString('pl-PL')
      };
      setEntries([entry, ...entries]);
      setNewEntry('');
    }
  };

  return (
    <div className="diary">
      <div className="diary-header">
        <h1>Mój Dziennik</h1>
        <p>Miejsce na Twoje przemyślenia i refleksje</p>
      </div>
      
      <div className="diary-content">
        <form onSubmit={handleAddEntry} className="entry-form">
          <textarea
            value={newEntry}
            onChange={(e) => setNewEntry(e.target.value)}
            placeholder="Co chcesz dzisiaj zapisać?"
            className="entry-input"
          />
          <button type="submit" className="add-entry-btn">
            Dodaj wpis
          </button>
        </form>

        <div className="entries-list">
          {entries.map(entry => (
            <div key={entry.id} className="entry-item">
              <div className="entry-date">{entry.date}</div>
              <div className="entry-text">{entry.text}</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default Diary;