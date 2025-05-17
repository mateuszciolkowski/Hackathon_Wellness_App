import React, { useState, useEffect } from 'react';
import './App.css';
import HomePage from './components/HomePage/HomePage';
import TopNav from './components/TopNav/TopNav';
import Navbar from './components/Navbar/Navbar';
import MainContent from './components/MainContent/MainContent';
import LoginModal from './components/LoginModal/LoginModal';
import RegisterModal from './components/LoginModal/RegisterModal';
import { isAuthenticated, getUser, logout } from './utils/authUtils';

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [user, setUser] = useState(null);
  const [activeComponent, setActiveComponent] = useState(null);
  const [showLoginModal, setShowLoginModal] = useState(false);
  const [showRegisterModal, setShowRegisterModal] = useState(false);

  // Efekt, który będzie wykonywany przy montowaniu komponentu
  useEffect(() => {
    // Dodajemy nasłuchiwanie na zdarzenie beforeunload, które jest wywoływane przed odświeżeniem strony
    const handleBeforeUnload = () => {
      logout(); // Wylogowujemy użytkownika
    };

    window.addEventListener('beforeunload', handleBeforeUnload);

    // Sprawdzamy, czy użytkownik jest zalogowany przy montowaniu komponentu
    if (isAuthenticated()) {
      setIsLoggedIn(true);
      setUser(getUser());
    }

    // Czyszczenie nasłuchiwania przy odmontowywaniu komponentu
    return () => {
      window.removeEventListener('beforeunload', handleBeforeUnload);
    };
  }, []);

  const handleLoginClick = () => {
    setShowLoginModal(true);
  };

  const handleCloseModal = () => {
    setShowLoginModal(false);
  };

  const handleLoginSuccess = (userData) => {
    setIsLoggedIn(true);
    setUser(userData);
    setShowLoginModal(false);
  };

  const handleRegisterClick = () => {
    setShowRegisterModal(true);
  };

  return (
    <div className="App">
      {!isLoggedIn && <TopNav 
        onLoginClick={handleLoginClick} 
        onRegisterClick={handleRegisterClick}
        isLoggedIn={isLoggedIn} 
        user={user} 
      />}
      {isLoggedIn ? (
        <>
          <Navbar onComponentChange={setActiveComponent} />
          <MainContent activeComponent={activeComponent} />
        </>
      ) : (
        <HomePage />
      )}
      {showLoginModal && (
        <LoginModal 
          onClose={handleCloseModal} 
          onLoginSuccess={handleLoginSuccess} 
        />
      )}
      {showRegisterModal && (
        <RegisterModal 
          onClose={() => setShowRegisterModal(false)}
        />
      )}
    </div>
  );
}

export default App;