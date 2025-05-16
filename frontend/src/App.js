import React, { useState } from 'react';
import './App.css';
import HomePage from './components/HomePage/HomePage';
import TopNav from './components/TopNav/TopNav';
import Navbar from './components/Navbar/Navbar';
import MainContent from './components/MainContent/MainContent';

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [activeComponent, setActiveComponent] = useState(null);

  return (
    <div className="App">
      {isLoggedIn ? (
        <>
          <Navbar onComponentChange={setActiveComponent} />
          <MainContent activeComponent={activeComponent} />
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