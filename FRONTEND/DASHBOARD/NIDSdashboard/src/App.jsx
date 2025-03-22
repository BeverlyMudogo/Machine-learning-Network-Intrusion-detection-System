import { useState } from 'react'
import './App.css'
import Header from './Header'
import Sidebar from './Sidebar'
import Home from './Home'
import axios from 'axios'
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom"
import Predictions from "./predictionspage"; // Import Predictions page
import PacketTrafficChart from './packetschart'

function App() {

  const [message, setMessage] = useState("");

  const startCapture = () => {
    axios.post("http://127.0.0.1:8000/api/start_capture/")
      .then(response => setMessage(response.data.message))
      .catch(error => console.error("Error:", error));
  };


  // Function to trigger predictions
  const PredictionTrigger = () => {
    axios.post("http://127.0.0.1:8000/api/start_prediction_trigger/")  // Ensure this endpoint exists
      .then(response => setMessage(response.data.message))
      .catch(error => console.error("Error:", error));
  };

  // Function to send alerts
  const alertsTrigger = () => {
    axios.post("http://127.0.0.1:8000/api/send_alert/")  // Ensure this endpoint exists
      .then(response => setMessage(response.data.message))
      .catch(error => console.error("Error:", error));
  };



  const [openSidebarToggle, setOpenSidebarToggle] = useState(false)

  const OpenSidebar = () => {
    setOpenSidebarToggle(!openSidebarToggle)
  }

  return (
    <Router>
    <div className='grid-container'> 
      <Header OpenSidebar={OpenSidebar}/>
      <Sidebar openSidebarToggle={openSidebarToggle} OpenSidebar={OpenSidebar}/>
      
      <Routes>
      <Route path='/' element={<Home onstartCapture={startCapture} onPredictionTrigger={PredictionTrigger} onalertsTrigger={alertsTrigger}/>}/>
      <Route path='/predictions' element={<Predictions />} />
      <Route path='/packet-capture' element={<PacketTrafficChart />} />
      </Routes>
      <p>{message}</p>

    </div>
    </Router>
  )
}

export default App
