// Używa zmiennej środowiskowej REACT_APP_API_URL, domyślnie localhost:8001
export const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8001';

export const ENDPOINTS = {
  GET_ALL_DAYS: `${API_URL}/api/questions_answers/history/1`,
  CREATE_DAY: `${API_URL}/api/days/`,
  GET_USER: `${API_URL}/api/users/1`,
  CREATE_QUESTIONS_ANSWERS: `${API_URL}/api/questions_answers/batch`,
  POST_LOGIN: `${API_URL}/api/users/login`,
  POST_REGISTER: `${API_URL}/api/users/register`,
  CHAT_CHAT: `${API_URL}/api/chat/send`,
  POST_CHART: `${API_URL}/api/chart/mood-chart/range`,
  GET_ADVICE: `${API_URL}/api/chat/daily-advice/1`,
};