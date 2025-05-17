import React, { useState, useEffect, useRef } from 'react';
import './AIHandler.css';
import { ENDPOINTS } from '../../config';


function AIHandler() {
  const [query, setQuery] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [history, setHistory] = useState([{
    role: 'assistant',
    content: 'Witaj! Jestem Twoim prywatnym AI psychologiem...'
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
    if (!query.trim()) return;
    
    setIsLoading(true);
    setHistory(prev => [...prev, { role: 'user', content: query }]);
    
    try {
      const response = await fetch(ENDPOINTS.CHAT_CHAT, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ prompt: query })
      });
      
      if (!response.ok) {
        throw new Error(`Błąd HTTP! status: ${response.status}`);
      }
      
      const data = await response.json();
      setHistory(prev => [...prev, { role: 'assistant', content: data.response }]);
    } catch (error) {
      console.error('Błąd podczas komunikacji z AI:', error);
      setHistory(prev => [...prev, { 
        role: 'assistant', 
        content: 'Przepraszam, serwer backend nie odpowiada. Upewnij się, że backend jest uruchomiony (komenda: python3 main.py w folderze backend)'
      }]);
    } finally {
      setIsLoading(false);
      setQuery('');
    }
  };

  return (
    <div className="ai-messenger-section">
      <div className="ai-history-section" ref={historyRef}>
        {history.map((item, index) => (
          <div key={index} className={`ai-message ${item.role}`}>
            <div className="message-header">
              {item.role === 'user' ? 'Ty' : 'AI Psycholog'}
            </div>
            <div className="message-content">{item.content}</div>
          </div>
        ))}
        {isLoading && (
          <div className="ai-message assistant">
            <div className="message-header">AI Psycholog</div>
            <div className="message-content">Piszę odpowiedź...</div>
          </div>
        )}
      </div>
      <form onSubmit={handleSubmit} className="ai-message-form">
        <textarea
          value={query}
          onChange={handleQueryChange}
          placeholder="Wpisz swoje zapytanie..."
          className="ai-query-input"
          disabled={isLoading}
        />
        <button 
          type="submit" 
          className="ai-submit-btn"
          disabled={isLoading || !query.trim()}
        >
          {isLoading ? 'Wysyłanie...' : 'Wyślij'}
        </button>
      </form>
    </div>
  );
}

export default AIHandler;