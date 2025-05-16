import React, { useRef } from 'react';
import './HomePage.css';

function HomePage() {
  const journalRef = useRef(null);
  const reportsRef = useRef(null);
  const growthRef = useRef(null);

  const scrollToSection = (ref) => {
    ref.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const scrollToTop = () => {
    window.scrollTo({
      top: 0,
      behavior: 'smooth'
    });
  };

  return (
    <div className="home-page">
      <div className="welcome-content">
        <div className="logo-container">
          <div className="animation-container">
            <div className="circle-animation"></div>
          </div>
          <div className="brand-name">Wellness</div>
        </div>
        <h1>Twoje miejsce spokoju i rozwoju</h1>
        <p>Zadbaj o swój wewnętrzny spokój i harmonię</p>
        
        <div className="nav-buttons">
          <button className="nav-button pink" onClick={() => scrollToSection(journalRef)}>
            <i className="icon-journal">📝</i>
            Tworzenie wpisów
          </button>
          <button className="nav-button orange" onClick={() => scrollToSection(reportsRef)}>
            <i className="icon-reports">📊</i>
            Generuj własne raporty
          </button>
          <button className="nav-button green" onClick={() => scrollToSection(growthRef)}>
            <i className="icon-growth">🌟</i>
            Rozwój
          </button>
        </div>

        <div className="sections">
          <section ref={journalRef} className="content-section pink-section">
            <h2>Tworzenie wpisów</h2>
            <div className="section-content">
              <p className="section-intro">Zapisuj swoje myśli, emocje i doświadczenia. Regularne prowadzenie dziennika pomoże Ci lepiej zrozumieć siebie i swoje samopoczucie.</p>
              
              <div className="features-grid">
                <div className="feature-card">
                  <div className="feature-header">
                    <span className="feature-icon">📝</span>
                    <h3>Codzienne zapiski</h3>
                  </div>
                  <p>Zacznij dzień od krótkiego wpisu – jak się dziś czujesz? Co Cię czeka? Zapisuj swoje przemyślenia i plany na przyszłość.</p>
                </div>

                <div className="feature-card">
                  <div className="feature-header">
                    <span className="feature-icon">😊</span>
                    <h3>Śledzenie nastroju</h3>
                  </div>
                  <p>Dodaj emotkę lub ocenę swojego nastroju. Monitoruj swoje samopoczucie i identyfikuj czynniki, które na nie wpływają.</p>
                </div>

                <div className="feature-card">
                  <div className="feature-header">
                    <span className="feature-icon">🎯</span>
                    <h3>Cele i osiągnięcia</h3>
                  </div>
                  <p>Zapisuj swoje cele i śledź postępy w ich realizacji. Świętuj małe i duże sukcesy na swojej drodze do rozwoju.</p>
                </div>

                <div className="feature-card">
                  <div className="feature-header">
                    <span className="feature-icon">💭</span>
                    <h3>Refleksje i wnioski</h3>
                  </div>
                  <p>Analizuj swoje doświadczenia i wyciągaj z nich wnioski. Buduj samoświadomość i rozwijaj się poprzez regularne przemyślenia.</p>
                </div>
              </div>

              <div className="benefits-section">
                <h3>Dlaczego warto prowadzić dziennik?</h3>
                <ul>
                  <li>Lepsze zrozumienie własnych emocji i zachowań</li>
                  <li>Redukcja stresu i napięcia</li>
                  <li>Możliwość śledzenia swojego rozwoju</li>
                  <li>Wsparcie w osiąganiu celów osobistych</li>
                </ul>
              </div>

              <div className="tips-section">
                <h3>Wskazówki do prowadzenia dziennika</h3>
                <ul>
                  <li>Pisz regularnie, najlepiej o stałej porze</li>
                  <li>Bądź szczery w swoich zapiskach</li>
                  <li>Nie oceniaj swoich myśli i uczuć</li>
                  <li>Wracaj do wcześniejszych wpisów i wyciągaj wnioski</li>
                </ul>
              </div>

              <div className="quote">
                „Pisanie to rozmowa z samym sobą. To pierwszy krok do zrozumienia swoich emocji i świadomego kierowania swoim życiem."
              </div>
            </div>
          </section>

          <section ref={reportsRef} className="content-section orange-section">
            <h2>Generowanie raportów</h2>
            <div className="section-content">
              <p className="section-intro">Twórz szczegółowe raporty swojego samopoczucia. Analizuj trendy i wzorce w swoich emocjach, aby lepiej zrozumieć swoje zdrowie psychiczne i dziel się nimi ze swoim psychologiem.</p>
              
              <div className="features-grid">
                <div className="feature-card">
                  <div className="feature-header">
                    <span className="feature-icon">📈</span>
                    <h3>Analiza trendów</h3>
                  </div>
                  <p>Śledź zmiany swojego nastroju w czasie i odkrywaj wzorce wpływające na Twoje samopoczucie. Generuj wykresy pokazujące Twój postęp.</p>
                </div>

                <div className="feature-card">
                  <div className="feature-header">
                    <span className="feature-icon">📊</span>
                    <h3>Statystyki i wykresy</h3>
                  </div>
                  <p>Twórz przejrzyste wizualizacje swoich postępów. Identyfikuj czynniki wpływające na Twoje samopoczucie.</p>
                </div>

                <div className="feature-card">
                  <div className="feature-header">
                    <span className="feature-icon">👥</span>
                    <h3>Wsparcie terapii</h3>
                  </div>
                  <p>Udostępniaj raporty swojemu psychologowi, aby efektywniej pracować nad swoim zdrowiem psychicznym podczas sesji terapeutycznych.</p>
                </div>

                <div className="feature-card">
                  <div className="feature-header">
                    <span className="feature-icon">🎯</span>
                    <h3>Cele i postępy</h3>
                  </div>
                  <p>Wyznaczaj cele związane ze zdrowiem psychicznym i monitoruj postępy w ich osiąganiu.</p>
                </div>
              </div>

              <div className="benefits-section">
                <h3>Korzyści z regularnego monitorowania</h3>
                <ul>
                  <li>Lepsze zrozumienie własnych emocji i zachowań</li>
                  <li>Efektywniejsza komunikacja z psychologiem</li>
                  <li>Możliwość śledzenia efektów terapii</li>
                  <li>Wczesne wykrywanie niepokojących wzorców</li>
                </ul>
              </div>

              <div className="quote">
                „Regularne monitorowanie to klucz do zrozumienia siebie i skutecznej terapii."
              </div>
            </div>
          </section>

          <section ref={growthRef} className="content-section green-section">
            <h2>Rozwój osobisty</h2>
            <div className="section-content">
              <p>Wspieraj swój rozwój osobisty poprzez regularne ćwiczenia i praktyki wspierające dobre samopoczucie.</p>
            </div>
          </section>
        </div>
      </div>
      
      <button 
        className="scroll-to-top-button"
        onClick={scrollToTop}
        aria-label="Przewiń do góry"
      >
        ↑
      </button>
    </div>
  );
}

export default HomePage;