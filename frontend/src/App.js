import React, { useState } from 'react';
import './App.css';
import HomePage from './components/HomePage/HomePage';
import TopNav from './components/TopNav/TopNav';
import MainMenu from './components/MainMenu/MainMenu';

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  return (
    <div className="App">
      {isLoggedIn ? (
        <>
          <MainMenu />
          <HomePage />
        </>
      ) : (
        <>
          <TopNav onLoginClick={() => setIsLoggedIn(true)} />
          <HomePage />
        </>
      )}
    </div>
  );
}

export default App;