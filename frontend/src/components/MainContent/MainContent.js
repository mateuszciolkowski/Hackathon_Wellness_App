import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './MainContent.css';
import Diary from '../Diary/Diary';
import User from '../User/User';
import History from '../History/History';
import AIHandler from '../AIHandler/AIHandler';
import { ENDPOINTS, API_URL } from '../../config';

function MainContent({ activeComponent }) {
    const [answers, setAnswers] = useState({
        question1: '',
        question2: '',
        question3: ''
    });
    const [questions, setQuestions] = useState({});
    const [hasEntries, setHasEntries] = useState(false);

    useEffect(() => {
        const checkAndFetchQuestions = async () => {
            try {
                const response = await axios.get(ENDPOINTS.GET_ALL_DAYS);
                const todayEntries = response.data.filter(entry => {
                    const entryDate = new Date(entry.created_at).toDateString();
                    const today = new Date().toDateString();
                    return entryDate === today;
                });

                setHasEntries(todayEntries.length > 0);

                try {
                    const questionsResponse = await axios.post(`${API_URL}/api/chat/generate-questions`, {
                        user_id: 9
                    });
                    
                    // Dodajemy dodatkowe sprawdzenie i debugowanie
                    if (!questionsResponse.data || !questionsResponse.data.response) {
                        console.error('Nieprawidłowa odpowiedź z API:', questionsResponse);
                        return;
                    }

                    // Parsujemy odpowiedź z podwójnym JSON.parse (bo response jest stringiem zawierającym string JSON)
                    const parsedResponse = JSON.parse(JSON.parse(questionsResponse.data.response));
                    
                    if (!parsedResponse.questions || !Array.isArray(parsedResponse.questions)) {
                        console.error('Nieprawidłowy format pytań:', parsedResponse);
                        return;
                    }

                    setQuestions({
                        question1: parsedResponse.questions[0] || '',
                        question2: parsedResponse.questions[1] || '',
                        question3: parsedResponse.questions[2] || ''
                    });
                } catch (error) {
                    console.error('Błąd podczas pobierania pytań:', error);
                }
            } catch (error) {
                console.error('Błąd podczas sprawdzania wpisów:', error);
            }
        };

        checkAndFetchQuestions();
    }, []);

    const handleAnswerChange = (questionKey, value) => {
        setAnswers(prev => ({
            ...prev,
            [questionKey]: value
        }));
    };

    const handleSubmitAll = async () => {
        try {
            const questionsAnswers = Object.entries(questions).map(([key, question]) => ({
                question: question,
                answer: answers[key]
            }));
    
            // Wysyłamy każde pytanie i odpowiedź osobno
            for (const qa of questionsAnswers) {
                const payload = {
                    day_id: 5,
                    questions_answers: [
                        {
                            question: qa.question,
                            answer: qa.answer,
                            day_id: 5
                        }
                    ]
                };
    
                await axios.post(`${ENDPOINTS.CREATE_QUESTIONS_ANSWERS}`, payload);
            }
            
            // Czyszczenie formularza po udanym wysłaniu
            setAnswers({
                question1: '',
                question2: '',
                question3: ''
            });
    
        } catch (error) {
            console.error('Błąd podczas wysyłania odpowiedzi:', error);
        }
    };

    const renderComponent = () => {
        switch (activeComponent) {
            case 'diary':
                return <div className="diary-section"><Diary /></div>;
            case 'user':
                return <div className="user-section"><User /></div>;
            case 'history':
                return <div className="history-section"><History /></div>;
            case 'aiHandler':
                return <div className="ai-handler-section"><AIHandler /></div>;
            default:
                return (
                    <div className="welcome-section">
                        <h1>Witaj w swojej przestrzeni wellness</h1>
                        <p>Zadbaj o swoje samopoczucie z naszymi narzędziami</p>
                        
                        <div className="questions-section">
                            <h2>Pytania na dziś:</h2>
                            <div className="questions-container">
                                {Object.entries(questions).map(([key, question]) => (
                                    <div key={key} className="question-item">
                                        <p>{question}</p>
                                        <textarea
                                            value={answers[key]}
                                            onChange={(e) => handleAnswerChange(key, e.target.value)}
                                            placeholder="Wpisz swoją odpowiedź..."
                                            className="entry-input"
                                        />
                                    </div>
                                ))}
                                <button 
                                    onClick={handleSubmitAll} 
                                    className="submit-all-btn"
                                    disabled={!Object.values(answers).some(answer => answer.trim() !== '')}
                                >
                                    Wyślij wszystkie odpowiedzi
                                </button>
                            </div>
                        </div>
                    </div>
                );
        }
    };

    return (
        <div className="main-content">
            {renderComponent()}
        </div>
    );
}

export default MainContent;