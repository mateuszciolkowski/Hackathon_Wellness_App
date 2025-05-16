import React, { useState } from 'react';
import './AIHandler.css';

function AIHandler() {
  const [query, setQuery] = useState('');
  const [response, setResponse] = useState('');
  const [history, setHistory] = useState([]);

  const handleQueryChange = (e) => {
    setQuery(e.target.value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const newResponse = 'Odpowiedź AI na Twoje zapytanie';
    setResponse(newResponse);
    setHistory([...history, { query, response: newResponse }]);
    setQuery('');
  };

  return (
      <div className="ai-messenger-section">
        <div className="ai-history-section">
          {history.map((item, index) => (
            <div key={index} className="ai-message-item">
              <div className="ai-message-query"><strong>Pytanie:</strong> {item.query}</div>
              <div className="ai-message-response"><strong>Odpowiedź:</strong> {item.response}</div>
            </div>
          ))}
        </div>
        <form onSubmit={handleSubmit} className="ai-message-form">
          <textarea
            value={query}
            onChange={handleQueryChange}
            placeholder="Wpisz swoje zapytanie..."
            className="ai-query-input"
          />
          <button type="submit" className="ai-submit-btn">Wyślij</button>
        </form>
      </div>
  );
}

export default AIHandler;