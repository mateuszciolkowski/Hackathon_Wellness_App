import React, { useState } from 'react';
import './App.css';
import HomePage from './components/HomePage/HomePage';
import LoginModal from './components/LoginModal/LoginModal';
import TopNav from './components/TopNav/TopNav';

function App() {
  const [isLoginModalOpen, setIsLoginModalOpen] = useState(false);

  return (
    <div className="App">
      <TopNav onLoginClick={() => setIsLoginModalOpen(true)} />
      <HomePage />
      {isLoginModalOpen && (
        <LoginModal onClose={() => setIsLoginModalOpen(false)} />
      )}
    </div>
  );
}

export default App;