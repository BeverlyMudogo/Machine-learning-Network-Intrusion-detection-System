import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Line } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js';

// Registering Chart.js components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

const TrafficPredictionChart = () => {
  const [chartData, setChartData] = useState({
    timestamps: [],
    predictions: [],
  });

  useEffect(() => {
    // Fetch data from your API endpoint
    axios.get('http://127.0.0.1:8000/api/get_predictions/')
      .then((response) => {
        // Process the response data
        const timestamps = response.data.map(item => new Date(item.timestamp).toLocaleTimeString()); // Convert timestamp to readable time
        const predictions = response.data.map(item => item.prediction);

        setChartData({
          timestamps,
          predictions,
        });
      })
      .catch((error) => {
        console.error('Error fetching predictions:', error);
      });
  }, []);



  // Prepare chart data
  const data = {
    labels: chartData.timestamps, // X-axis: timestamps
    datasets: [
      {
        label: 'Prediction',
        data: chartData.predictions, // Y-axis: predictions
        borderColor: 'rgba(75, 192, 192, 1)',
        backgroundColor: 'rgba(75, 192, 192, 0.2)',
        fill: false,
        tension: 0.1,
      },
    ],
  };

  // Chart.js options
  const options = {
    responsive: true,
    scales: {
      x: {
        title: {
          display: true,
          text: 'Time (HH:MM:SS)',
        },
        ticks: {
          autoSkip: true, // Skips every other label to avoid overlap
          maxRotation: 45,
          minRotation: 45,
        },
      },
      y: {
        title: {
          display: true,
          text: 'Prediction Value',
        },
        beginAtZero: true,
      },
    },
  };

  return (
    <div style={{ width: '80%', margin: '0 auto' }}>
      <h2 style={{ textAlign: 'center', color: '#7a7f85', marginBottom: '20px' }}>Traffic Prediction Over Time</h2>
      <Line data={data} options={options} />
    </div>
  );
};

export default TrafficPredictionChart;
