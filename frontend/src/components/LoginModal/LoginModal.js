import React, { useRef } from 'react';
import axios from 'axios';
import './LoginModal.css';
import { API_URL, ENDPOINTS } from '../../config';
import { saveSession } from '../../utils/authUtils';

// Konfiguracja bazowego URL dla Axios
axios.defaults.baseURL = API_URL;

function LoginModal({ onClose, onLoginSuccess }) {
  const emailRef = useRef(null);
  const passwordRef = useRef(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    const email = emailRef.current.value;
    const password = passwordRef.current.value;
    
    try {
      // Poprawne wywołanie axios.post
      const response = await axios.post(ENDPOINTS.POST_LOGIN, {
        email: email,
        password: password
      });
      
      // Zapisz dane sesji
      const userData = response.data;
      saveSession(userData);
      
      // Powiadom rodzica o udanym logowaniu
      if (onLoginSuccess) {
        onLoginSuccess(userData);
      }
      
      onClose();
    } catch (err) {
      console.error('Błąd logowania:', err);
      alert('Wystąpił błąd podczas logowania. Spróbuj ponownie.');
    }
  };

  return (
    <div className="modal-overlay">
      <div className="modal-content">
        <button className="close-button" onClick={onClose}>×</button>
        <h2>Logowanie</h2>
        <form onSubmit={handleSubmit}>
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
          <button 
            type="submit" 
            className="login-submit"
          >
            Zaloguj się
          </button>
        </form>
      </div>
    </div>
  );
}

export default LoginModal;