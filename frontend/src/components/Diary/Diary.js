<<<<<<< HEAD
import React, { useState } from 'react';
import axios from 'axios';
import './Diary.css';
import { ENDPOINTS } from '../../config';

function Diary() {
  const [entries, setEntries] = useState([]);
  const [newEntry, setNewEntry] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState(null);
  const [showModal, setShowModal] = useState(false);
  const [mood, setMood] = useState(null);
  const [fadeOut, setFadeOut] = useState(false);

  const handleMoodSelection = (index) => {
    setMood(index);
    setFadeOut(true);
    setTimeout(() => {
      setShowModal(false);
      setFadeOut(false);
    }, 2000);
  };

  const handleAddEntry = async (e) => {
    e.preventDefault();
    if (newEntry.trim() === '' || mood === null) {
      setError('Proszę wybrać nastrój i wpisać treść przed dodaniem wpisu.');
      return;
    }

    setIsSubmitting(true);
    setError(null);

    try {
      const entryData = {
        user_id: 1,
        main_entry: newEntry,
        day_rating: (mood * 20) // Zmiana z ((mood + 1) * 20) na (mood * 20)
      };

      const response = await axios.post(ENDPOINTS.CREATE_DAY, entryData);
      
      const entry = {
        id: response.data.id,
        text: newEntry,
        date: new Date().toLocaleDateString('pl-PL'),
        mood: ['😢', '😕', '😐', '🙂', '😊'][mood]
      };

      setEntries([entry, ...entries]);
      setNewEntry('');
      setMood(null);
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
        <button onClick={() => setShowModal(true)} className="open-modal-btn">
          {mood !== null ? ['😢', '😕', '😐', '🙂', '😊'][mood] : 'Wybierz nastrój'}
        </button>
        
        {showModal && (
          <div className={`modal ${fadeOut ? 'fade-out' : ''}`}>
            <div className="modal-content">
              <span className="close-btn" onClick={() => setShowModal(false)}>&times;</span>
              <h2>Jak się dziś czujesz?</h2>
              <div className="mood-options">
                {['😢', '😕', '😐', '🙂', '😊'].map((emoji, index) => (
                  <span
                    key={index}
                    className={`mood-option ${mood === index ? 'selected' : ''}`}
                    onClick={() => handleMoodSelection(index)}
                  >
                    {emoji}
                  </span>
                ))}
              </div>
            </div>
          </div>
        )}

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
            disabled={isSubmitting || mood === null}
          >
            {isSubmitting ? 'Dodawanie...' : 'Dodaj wpis'}
          </button>
        </form>

        <div className="entries-list">
          {entries.map(entry => (
            <div key={entry.id} className="entry-item">
              <div className="entry-date">{entry.date}</div>
              <div className="entry-mood">{entry.mood}</div>
              <div className="entry-text">{entry.text}</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

=======
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

      const response = await axios.post('/api/da', entryData);
      
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

>>>>>>> back
export default Diary;