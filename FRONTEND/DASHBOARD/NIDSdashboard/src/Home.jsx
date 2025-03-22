import React from 'react'
import { MdNetworkCheck } from "react-icons/md" // network check (packet capture engine) icon
import { MdOutlineOnlinePrediction } from "react-icons/md" // pred icon
import {BsFillBellFill} from "react-icons/bs" // alerts
import TrafficPredictionChart from './chart'; // Import the chart component


function Home({onstartCapture, onPredictionTrigger, onalertsTrigger}){

    

    return (
        <main className='main-container'>
            <div className='main-title'>
                <h3>DASHBOARD</h3>
            </div>

            <div className='main-cards'>
                <div className='card' onClick={onstartCapture} >
                    <div className='card-inner'> 
                        <h3>Start Packet Capture</h3>
                        <MdNetworkCheck className='card-icon'/>
                    </div>
                    <h4>Real time pcap</h4>
                </div>

                <div className='card' onClick={onPredictionTrigger}>
                    <div className='card-inner'> 
                        <h3>Predict</h3>
                        <MdOutlineOnlinePrediction className='card-icon'/>
                    </div>
                    <h4>Real-time Prediction</h4>
                </div>

                <div className='card' onClick={onalertsTrigger}>
                    <div className='card-inner'> 
                        <h3>Alerts</h3>
                        <BsFillBellFill className='card-icon'/>
                    </div>
                    <h4>Intrusion Alert</h4>
                </div>
            </div>

            {/* Line Chart Section */}
      <div className='chart-container'>
        <TrafficPredictionChart /> {/* Render the TrafficPredictionChart component here */}
      </div>

            
        </main>
    )
}

export default Home