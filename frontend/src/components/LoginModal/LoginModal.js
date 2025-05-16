import React from 'react';
import './LoginModal.css';

function LoginModal({ onClose }) {
  const handleSubmit = (e) => {
    e.preventDefault();
    // Tutaj dodasz logikę logowania
    onClose();
  };

  return (
    <div className="modal-overlay">
      <div className="modal-content">
        <button className="close-button" onClick={onClose}>×</button>
        <h2>Logowanie</h2>
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <input
              type="text"
              placeholder="Nazwa użytkownika"
              required
            />
          </div>
          <div className="form-group">
            <input
              type="password"
              placeholder="Hasło"
              required
            />
          </div>
          <button type="submit" className="login-submit">Zaloguj się</button>
        </form>
      </div>
    </div>
  );
}

export default LoginModal;