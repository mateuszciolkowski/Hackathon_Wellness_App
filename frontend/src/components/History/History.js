import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './History.css';
import { ENDPOINTS } from '../../config';

function History() {
  const [entries, setEntries] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedEntry, setSelectedEntry] = useState(null);

  useEffect(() => {
    const fetchEntries = async () => {
      try {
        const response = await axios.get(ENDPOINTS.GET_ALL_DAYS);
        setEntries(response.data);
        setLoading(false);
      } catch (err) {
        setError('Nie udało się pobrać wpisów. Spróbuj ponownie później.');
        setLoading(false);
      }
    };

    fetchEntries();
  }, []);

  if (loading) return <div className="loading">Ładowanie wpisów...</div>;
  if (error) return <div className="error">{error}</div>;

  const truncateText = (text, maxLength = 50) => {
    if (!text) return '';
    if (text.length <= maxLength) return text;
    return text.substring(0, maxLength) + '...';
  };

  const handleEntryClick = (entry) => {
    setSelectedEntry(entry);
  };

  return (
    <div className="history-container">
      <div className="history-header">
        <h2>Moje Wpisy</h2>
        <p>Historia Twoich przemyśleń i doświadczeń</p>
      </div>
      
      <div className="entries-timeline">
        {entries.map(entry => (
          <div 
            key={entry.id} 
            className="entry-card"
            onClick={() => handleEntryClick(entry)}
          >
            <div className="entry-date">
              <span className="date-day">{new Date(entry.created_at).getDate()}</span>
              <span className="date-month">
                {new Date(entry.created_at).toLocaleString('pl-PL', { month: 'short' })}
              </span>
            </div>
            <div className="entry-content">
              <div className="entry-mood">
                {entry.day_rating >= 80 ? "😊" : 
                 entry.day_rating >= 60 ? "🙂" :
                 entry.day_rating >= 40 ? "😐" :
                 entry.day_rating >= 20 ? "😕" : "😢"}
              </div>
              <p>{truncateText(entry.main_entry)}</p>
              <div className="entry-rating">
                Ocena dnia: {entry.day_rating}/100
              </div>
            </div>
          </div>
        ))}
      </div>

      {selectedEntry && (
        <div className="modal" onClick={() => setSelectedEntry(null)}>
          <div className="modal-content" onClick={e => e.stopPropagation()}>
            <span className="close-btn" onClick={() => setSelectedEntry(null)}>&times;</span>
            <div className="modal-entry-date">
              {new Date(selectedEntry.created_at).toLocaleDateString('pl-PL')}
            </div>
            <div className="modal-entry-mood">
              {selectedEntry.day_rating >= 80 ? "😊" : 
               selectedEntry.day_rating >= 60 ? "🙂" :
               selectedEntry.day_rating >= 40 ? "😐" :
               selectedEntry.day_rating >= 20 ? "😕" : "😢"}
            </div>
            <div className="modal-entry-content">
              {selectedEntry.main_entry}
            </div>
            <div className="modal-entry-rating">
              Ocena dnia: {selectedEntry.day_rating}/100
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default History;