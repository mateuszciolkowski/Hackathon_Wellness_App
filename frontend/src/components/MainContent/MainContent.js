<<<<<<< HEAD
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

=======
import React, { useState } from 'react';
import './MainContent.css';
import Diary from '../Diary/Diary';
import User from '../User/User';
import History from '../History/History';
import AIHandler from '../AIHandler/AIHandler'; // Dodaj ten import

function MainContent({ activeComponent }) {
    const [mood, setMood] = useState(null);
    const [showModal, setShowModal] = useState(false);
    const [answers, setAnswers] = useState({});
    const [fadeOut, setFadeOut] = useState(false);

    const handleMoodSelection = (index) => {
        setMood(index);
        setFadeOut(true);
        setTimeout(() => {
            setShowModal(false);
            setFadeOut(false);
        }, 2000); // 2 seconds for fade out
        // Here you can add logic to save the selection, e.g., sending to the backend
    };

    const handleAnswerChange = (question, value) => {
        setAnswers({ ...answers, [question]: value });
    };

    const handleSubmit = (question) => {
        // Here you can add logic to send the answer, e.g., sending to the backend
        console.log(`Answer to question "${question}": ${answers[question]}`);
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
                return <div className="ai-handler-section"><AIHandler /></div>; // Poprawka tutaj
            default:
                return (
                    <div className="welcome-section">
                        <h1>Welcome to your wellness space</h1>
                        <p>Take care of your mental health with our tools</p>
                        <button onClick={() => setShowModal(true)} className="open-modal-btn">Choose Mood</button>
                        {showModal && (
                            <div className={`modal ${fadeOut ? 'fade-out' : ''}`}>
                                <div className="modal-content">
                                    <span className="close-btn" onClick={() => setShowModal(false)}>&times;</span>
                                    <h2>How do you feel today?</h2>
                                    <div className="mood-options">
                                        {['😢', '😕', '😐', '🙂', '😊'].map((emoji, index) => (
                                            <span
                                                key={index}
                                                className={`mood-option ${mood === index ? 'selected' : ''}`}
                                                onClick={() => handleMoodSelection(index)}
                                            >
                                                {emoji}
                                            </span>
                                        ))}
                                    </div>
                                </div>
                            </div>
                        )}
                        <div className="questions-section">
                            <h2>Daily Questions:</h2>
                            <ul>
                                {['How do you feel today?', 'What made you happy?', 'What are your plans for tomorrow?'].map((question, index) => (
                                    <li key={index} className="question-item">
                                        <p>{question}</p>
                                        <textarea
                                            value={answers[question] || ''}
                                            onChange={(e) => handleAnswerChange(question, e.target.value)}
                                            placeholder="Enter your answer..."
                                            className="entry-input"
                                        />
                                        <button onClick={() => handleSubmit(question)} className="add-entry-btn">Submit</button>
                                    </li>
                                ))}
                            </ul>
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

>>>>>>> back
export default MainContent;