import React, { useState, useEffect, useRef } from 'react';
import './AIHandler.css';

function AIHandler() {
  const [query, setQuery] = useState('');
  const [response, setResponse] = useState('');
  const [history, setHistory] = useState([]);
  const historyRef = useRef(null);

  useEffect(() => {
    if (historyRef.current) {
      historyRef.current.scrollTop = historyRef.current.scrollHeight;
    }
  }, [history]);

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
      <div className="ai-history-section" ref={historyRef}>
        {history.map((item, index) => (
          <div key={index} className="ai-conversation-item">
            <div className="ai-query-container">
              <div className="ai-message-query">
                <div className="message-header">Twoje pytanie:</div>
                {item.query}
              </div>
            </div>
            <div className="ai-response-container">
              <div className="ai-message-response">
                <div className="message-header">Odpowiedź AI:</div>
                {item.response}
              </div>
            </div>
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