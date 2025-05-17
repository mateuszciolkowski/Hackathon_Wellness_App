<<<<<<< HEAD
import React, { useState, useEffect, useRef } from 'react';
import './AIHandler.css';

function AIHandler() {
  const [query, setQuery] = useState('');
  const [response, setResponse] = useState('');
  const [history, setHistory] = useState([{
    response: 'Witaj! Jestem Twoim prywatnym AI psychologiem. Jestem tu, aby Ci pomóc w trudnych chwilach, odpowiedzieć na nurtujące Cię pytania i wspierać Cię w rozwoju osobistym. Możesz mi zaufać i podzielić się swoimi przemyśleniami - jestem tu, aby Cię wysłuchać i pomóc znaleźć najlepsze rozwiązania. O czym chciałbyś/chciałabyś porozmawiać?'
  }]);
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
            {item.query && (
              <div className="ai-query-container">
                <div className="ai-message-query">
                  <div className="message-header">Twoje pytanie:</div>
                  {item.query}
                </div>
              </div>
            )}
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

=======
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

>>>>>>> back
export default AIHandler;