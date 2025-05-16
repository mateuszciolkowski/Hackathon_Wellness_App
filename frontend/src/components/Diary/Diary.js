import React, { useState } from 'react';
import axios from 'axios';
import './Diary.css';
import { ENDPOINTS } from '../../config';

function Diary() {
  const [entries, setEntries] = useState([]);
  const [newEntry, setNewEntry] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState(null);

  const handleAddEntry = async (e) => {
    e.preventDefault();
    if (newEntry.trim() === '') return;

    setIsSubmitting(true);
    setError(null);

    try {
      const entryData = {
        user_id: 1, // Na razie ustawione na stałe
        main_entry: newEntry,
        day_rating: 50 // Możesz dodać pole do oceny dnia w formularzu
      };

      const response = await axios.post(ENDPOINTS.CREATE_DAY, entryData);
      
      const entry = {
        id: response.data.id,
        text: newEntry,
        date: new Date().toLocaleDateString('pl-PL')
      };

      setEntries([entry, ...entries]);
      setNewEntry('');
      setIsSubmitting(false);
    } catch (err) {
      setError('Nie udało się dodać wpisu. Spróbuj ponownie później.');
      setIsSubmitting(false);
    }
  };

  return (
    <div className="diary">
      <div className="diary-header">
        <h1>Mój Pamiętnik</h1>
        <p>Miejsce na Twoje przemyślenia i refleksje</p>
      </div>
      
      <div className="diary-content">
        <form onSubmit={handleAddEntry} className="entry-form">
          <textarea
            value={newEntry}
            onChange={(e) => setNewEntry(e.target.value)}
            placeholder="Co chcesz dzisiaj zapisać?"
            className="entry-input"
            disabled={isSubmitting}
          />
          {error && <div className="error-message">{error}</div>}
          <button 
            type="submit" 
            className="add-entry-btn"
            disabled={isSubmitting}
          >
            {isSubmitting ? 'Dodawanie...' : 'Dodaj wpis'}
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