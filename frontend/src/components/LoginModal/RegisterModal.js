import React, { useRef } from 'react';
import axios from 'axios';
import './LoginModal.css';
import { API_URL, ENDPOINTS } from '../../config';

function RegisterModal({ onClose }) {
  const emailRef = useRef(null);
  const passwordRef = useRef(null);
  const nameRef = useRef(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    try {
      const response = await axios.post(ENDPOINTS.POST_REGISTER, {
        email: emailRef.current.value,
        password: passwordRef.current.value,
        name: nameRef.current.value
      });
      
      alert('Rejestracja zakończona sukcesem! Możesz się teraz zalogować.');
      onClose();
    } catch (err) {
      console.error('Błąd rejestracji:', err);
      alert('Wystąpił błąd podczas rejestracji. Spróbuj ponownie.');
    }
  };

  return (
    <div className="modal-overlay">
      <div className="modal-content">
        <button className="close-button" onClick={onClose}>×</button>
        <h2>Rejestracja</h2>
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <input
              type="text"
              name="name"
              placeholder="Imię"
              ref={nameRef}
              required
            />
          </div>
          <div className="form-group">
            <input
              type="email"
              name="email"
              placeholder="Email"
              ref={emailRef}
              required
            />
          </div>
          <div className="form-group">
            <input
              type="password"
              name="password"
              placeholder="Hasło"
              ref={passwordRef}
              required
            />
          </div>
          <button type="submit" className="login-submit">
            Zarejestruj się
          </button>
        </form>
      </div>
    </div>
  );
}

export default RegisterModal;