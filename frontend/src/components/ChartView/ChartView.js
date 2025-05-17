import React from 'react';
import axios from 'axios';
import { ENDPOINTS } from '../../config';
import './ChartView.css';

const ChartView = () => {
  const [loading, setLoading] = React.useState(false);
  const [error, setError] = React.useState(null);
  const [data, setData] = React.useState(null);

  React.useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      try {
        const response = await axios.post(ENDPOINTS.POST_CHART, {
          diary_id: 1,
          start_date: "2025-05-10",
          end_date: "2025-05-17"
        });

        if (response.data && response.data.dates && response.data.ratings) {
          setData(response.data);
          
          // Rysowanie wykresu za pomocą Canvas API
          const canvas = document.createElement('canvas');
          const ctx = canvas.getContext('2d');
          
          // Zmniejszamy szerokość canvas
          canvas.width = 600;
          canvas.height = 400;
          
          // Czyszczenie canvas
          ctx.clearRect(0, 0, canvas.width, canvas.height);
          
          // Style dla wykresu
          ctx.strokeStyle = '#4CAF50';
          ctx.lineWidth = 2;
          ctx.font = '12px Arial';
          
          // Marginesy
          const margin = { top: 40, right: 40, bottom: 40, left: 60 };
          const width = canvas.width - margin.left - margin.right;
          const height = canvas.height - margin.top - margin.bottom;
          
          // Rysowanie osi
          ctx.beginPath();
          ctx.moveTo(margin.left, canvas.height - margin.bottom);
          ctx.lineTo(canvas.width - margin.right, canvas.height - margin.bottom); // oś X
          ctx.moveTo(margin.left, margin.top);
          ctx.lineTo(margin.left, canvas.height - margin.bottom); // oś Y
          ctx.strokeStyle = '#000';
          ctx.stroke();
          
          // Rysowanie punktów danych
          const xStep = width / (response.data.dates.length - 1);
          const yScale = height / 100; // zakładamy, że wartości są od 0 do 100
          
          ctx.beginPath();
          ctx.strokeStyle = '#4CAF50';
          response.data.ratings.forEach((value, index) => {
            const x = margin.left + (xStep * index);
            const y = canvas.height - margin.bottom - (value * yScale);
            
            if (index === 0) {
              ctx.moveTo(x, y);
            } else {
              ctx.lineTo(x, y);
            }
            
            // Dodawanie punktów
            ctx.fillStyle = '#4CAF50';
            ctx.beginPath();
            ctx.arc(x, y, 4, 0, Math.PI * 2);
            ctx.fill();
            
            // Dodawanie etykiet dat
            ctx.fillStyle = '#000';
            ctx.fillText(response.data.dates[index], x - 20, canvas.height - margin.bottom + 20);
          });
          
          ctx.stroke();
          
          // Dodawanie etykiet osi Y
          for (let i = 0; i <= 100; i += 20) {
            const y = canvas.height - margin.bottom - (i * yScale);
            ctx.fillStyle = '#000';
            ctx.fillText(i.toString(), margin.left - 25, y + 5);
          }
          
          // Dodajemy canvas do DOM
          const chartDiv = document.getElementById('chart_div');
          chartDiv.innerHTML = '';
          chartDiv.appendChild(canvas);
          
          // Centrujemy canvas
          canvas.style.display = 'block';
          canvas.style.margin = '0 auto';
        }
      } catch (err) {
        setError('Wystąpił błąd podczas pobierania danych');
        console.error('Błąd:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  return (
    <div className="chart-container">
      <h2>Analiza Twojego Samopoczucia</h2>
      <div className="chart-wrapper">
        {loading && <p>Ładowanie danych...</p>}
        {error && <p className="error">{error}</p>}
        <div id="chart_div" style={{ 
          width: '100%', 
          height: '400px',
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center'
        }}></div>
      </div>
      <button className="export-button" onClick={() => {}}>
        Eksportuj do pliku
      </button>
      <div className="chart-usage">
        <h3>Zastosowanie wykresu:</h3>
        <ul>
          <li>Monitorowanie zmian nastroju w czasie</li>
          <li>Identyfikacja wzorców wpływających na samopoczucie</li>
          <li>Analiza skuteczności stosowanych terapii i działań</li>
          <li>Wsparcie w komunikacji z lekarzem lub terapeutą</li>
          <li>Lepsze zrozumienie własnego zdrowia psychicznego</li>
        </ul>
      </div>
    </div>
  );
};

export default ChartView;