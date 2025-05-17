// Funkcje pomocnicze do zarządzania sesją logowania

// Zapisuje dane sesji w localStorage
export const saveSession = (userData) => {
  localStorage.setItem('token', userData.access_token);
  localStorage.setItem('token_type', userData.token_type);
  localStorage.setItem('user', JSON.stringify({
    id: userData.id,
    email: userData.email,
    name: userData.name
  }));
  localStorage.setItem('session', JSON.stringify(userData));
};

// Pobiera dane sesji z localStorage
export const getSession = () => {
  const sessionData = localStorage.getItem('session');
  return sessionData ? JSON.parse(sessionData) : null;
};

// Pobiera token z localStorage
export const getToken = () => {
  return localStorage.getItem('token');
};

// Pobiera dane użytkownika z localStorage
export const getUser = () => {
  const userData = localStorage.getItem('user');
  return userData ? JSON.parse(userData) : null;
};

// Sprawdza, czy użytkownik jest zalogowany
export const isAuthenticated = () => {
  return !!getToken();
};

// Wylogowuje użytkownika
export const logout = () => {
  localStorage.removeItem('token');
  localStorage.removeItem('token_type');
  localStorage.removeItem('user');
  localStorage.removeItem('session');
};