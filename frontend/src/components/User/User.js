import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './User.css';
import { ENDPOINTS } from '../../config';

function User() {
  const [userData, setUserData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchUserData = async () => {
      try {
        const response = await axios.get(ENDPOINTS.GET_USER);
        setUserData(response.data);
        setLoading(false);
      } catch (err) {
        setError('Nie udało się pobrać danych użytkownika. Spróbuj ponownie później.');
        setLoading(false);
      }
    };

    fetchUserData();
  }, []);

  if (loading) return <div className="loading">Ładowanie danych użytkownika...</div>;
  if (error) return <div className="error">{error}</div>;
  if (!userData) return null;

  return (
    <div className="user-container">
      <div className="user-header">
        <h2>Profil Użytkownika</h2>
      </div>
      
      <div className="user-info">
        <div className="info-group">
          <label>Imię i Nazwisko:</label>
          <span>{userData.name}</span>
        </div>
        <div className="info-group">
          <label>Nickname:</label>
          <span>{userData.nickname}</span>
        </div>
        <div className="info-group">
          <label>Email:</label>
          <span>{userData.email}</span>
        </div>
        <div className="info-group">
          <label>Rok urodzenia:</label>
          <span>{userData.birth_year}</span>
        </div>
      </div>
    </div>
  );
}

export default User;