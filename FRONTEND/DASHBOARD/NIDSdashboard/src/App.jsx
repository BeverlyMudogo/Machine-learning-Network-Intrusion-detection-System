import { useState } from 'react';
import './App.css';
import Header from './Header';
import Sidebar from './Sidebar';
import Home from './Home';
import axios from 'axios';
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Predictions from "./predictionspage";
import PacketTrafficChart from './packetschart';

function App() {
  const [message, setMessage] = useState("");
  const [openSidebarToggle, setOpenSidebarToggle] = useState(false);

  const apiUrl = window.location.hostname.includes("railway")
    ? "https://postgres-production-1ba4.up.railway.app"
    : "http://127.0.0.1:8000";

  // Generic API function
  const callAPI = async (endpoint) => {
    try {
      const response = await axios.post(`${apiUrl}${endpoint}`);
      setMessage(response.data.message);
    } catch (error) {
      console.error("Error:", error);
    }
  };

  return (
    <Router>
      <div className='grid-container'>
        <Header OpenSidebar={() => setOpenSidebarToggle(prev => !prev)} />
        <Sidebar openSidebarToggle={openSidebarToggle} OpenSidebar={() => setOpenSidebarToggle(prev => !prev)} />
        
        <Routes>
          <Route path='/' element={<Home onstartCapture={() => callAPI("/api/start_capture/")} onPredictionTrigger={() => callAPI("/api/start_prediction_trigger/")} onalertsTrigger={() => callAPI("/api/send_alert/")} />} />
          <Route path='/predictions' element={<Predictions />} />
          <Route path='/packet-capture' element={<PacketTrafficChart />} />
        </Routes>
        
        <p>{message}</p>
      </div>
    </Router>
  );
}

export default App;
