import React, { useRef } from 'react';
import axios from 'axios';
import './LoginModal.css';
import { API_URL, ENDPOINTS } from '../../config';

function RegisterModal({ onClose }) {
  const emailRef = useRef(null);
  const passwordRef = useRef(null);
  const nameRef = useRef(null);
  const nicknameRef = useRef(null); 
  const birthYearRef = useRef(null); 

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    const birthYearInt = parseInt(birthYearRef.current.value, 10);

    if (isNaN(birthYearInt)) {
        alert('Rok urodzenia musi być poprawną liczbą.');
        return;
    }

    try {
      const response = await axios.post(ENDPOINTS.POST_REGISTER, {
        name: nameRef.current.value,
        nickname: nicknameRef.current.value, 
        email: emailRef.current.value,
        password: passwordRef.current.value,
        birth_year: birthYearInt 
      });
      
      alert('Rejestracja zakończona sukcesem! Możesz się teraz zalogować.');
      onClose();
    } catch (err) {
      console.error('Błąd rejestracji:', err);
      
      let errorMessage = 'Wystąpił nieznany błąd podczas rejestracji. Spróbuj ponownie.';
      
      if (err.response && err.response.data && err.response.data.detail) {
          if (Array.isArray(err.response.data.detail)) {
             errorMessage = 'Błąd walidacji danych: ' + err.response.data.detail.map(d => d.msg).join(', ');
          } else if (typeof err.response.data.detail === 'string') {
             errorMessage = err.response.data.detail;
          }
      }
      
      alert(`Błąd rejestracji: ${errorMessage}`);
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
              type="text"
              name="nickname"
              placeholder="Nazwa użytkownika (Nickname)"
              ref={nicknameRef}
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
              type="number" 
              name="birth_year"
              placeholder="Rok urodzenia"
              ref={birthYearRef}
              required
              min="1900"
              max={new Date().getFullYear()}
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