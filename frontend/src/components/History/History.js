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

  const formatDate = (dateString) => {
    const options = { 
      weekday: 'long', 
      year: 'numeric', 
      month: 'long', 
      day: 'numeric' 
    };
    return new Date(dateString).toLocaleDateString('pl-PL', options);
  };

  const openModal = (entry) => {
    setSelectedEntry(entry);
  };

  const closeModal = () => {
    setSelectedEntry(null);
  };

  return (
    <div className="history-container">
      <div className="history-header">
        <h2>Moje Wpisy</h2>
        <p>Historia Twoich przemyśleń i doświadczeń</p>
      </div>
      
      <div className="entries-timeline">
        {entries.map(entry => (
          <div key={entry.day_id} className="entry-card">
            <div className="entry-header">
              <div className="entry-date">{formatDate(entry.created_at)}</div>
              <div className="entry-rating">
                <span className="mood-emoji">
                  {entry.day_rating >= 80 ? "😊" : 
                   entry.day_rating >= 60 ? "🙂" :
                   entry.day_rating >= 40 ? "😐" :
                   entry.day_rating >= 20 ? "😕" : "😢"}
                </span>
                <span className="rating-text">
                  Samopoczucie: {entry.day_rating}/100
                </span>
              </div>
            </div>
            
            <div className="main-entry" onClick={() => openModal(entry)} style={{ cursor: 'pointer' }}>
              <p>{entry.main_entry}</p>
            </div>
            
            <div className="questions-container">
              {entry.questions.map(qa => (
                <div key={qa.id} className="qa-pair">
                  <div className="question">
                    <span className="question-icon">❓</span>
                    {qa.question}
                  </div>
                  <div className="answer">
                    <span className="answer-icon">💭</span>
                    {qa.answer}
                  </div>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>

      {selectedEntry && (
        <div className="entry-modal-overlay" onClick={closeModal}>
          <div className="entry-modal-content" onClick={e => e.stopPropagation()}>
            <button className="entry-modal-close" onClick={closeModal}>×</button>
            <h3>{formatDate(selectedEntry.created_at)}</h3>
            <div className="entry-modal-text">
              {selectedEntry.main_entry}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default History;