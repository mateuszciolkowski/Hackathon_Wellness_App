import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './History.css';
import { ENDPOINTS } from '../../config';

function History() {
  const [entries, setEntries] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

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
              <span className="date-day">{new Date(entry.created_at).getDate()}</span>
              <span className="date-month">
                {new Date(entry.created_at).toLocaleString('pl-PL', { month: 'short' })}
              </span>
            </div>
            <div className="entry-content">
              <div className="entry-mood">
                {entry.day_rating >= 80 ? "😊" : 
                 entry.day_rating >= 50 ? "😐" : "😔"}
              </div>
              <p>{entry.main_entry}</p>
              <div className="entry-rating">
                Ocena dnia: {entry.day_rating}/100
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default History;