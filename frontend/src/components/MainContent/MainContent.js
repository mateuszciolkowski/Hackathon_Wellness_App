import React, { useState } from 'react';
import axios from 'axios';
import './MainContent.css';
import Diary from '../Diary/Diary';
import User from '../User/User';
import History from '../History/History';
import AIHandler from '../AIHandler/AIHandler';
import { ENDPOINTS } from '../../config';

function MainContent({ activeComponent }) {
    const [answers, setAnswers] = useState({
        question1: '',
        question2: '',
        question3: ''
    });

    const questions = {
        question1: 'Jak się dzisiaj czujesz?',
        question2: 'Co sprawiło Ci dzisiaj radość?',
        question3: 'Jakie masz plany na jutro?'
    };

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

            const payload = {
                questions_answers: questionsAnswers
            };

            await axios.post(`${ENDPOINTS.CREATE_QUESTIONS_ANSWERS}`, payload);
            
            // Wyczyść odpowiedzi po udanym wysłaniu
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