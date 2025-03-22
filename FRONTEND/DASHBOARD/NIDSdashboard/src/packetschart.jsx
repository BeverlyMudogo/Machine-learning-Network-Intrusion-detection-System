import React, { useState, useEffect } from "react";
import { Line } from "react-chartjs-2";
import axios from "axios";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";

// Register ChartJS components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

function PacketTrafficChart() {
  const [packetData, setPacketData] = useState([]);

  // Fetch the packet data
  useEffect(() => {
    axios
      .get("http://127.0.0.1:8000/api/get_packets")
      .then((response) => {
        setPacketData(response.data);
      })
      .catch((error) => {
        console.error("Error fetching packet data:", error);
      });
  }, []);

  // Prepare data for the chart
  const prepareChartData = () => {
    // Here I'm using packet ID as time (assuming sequential)
    const packetTimes = packetData.map((item) => item.id); // Using ID as time for simplicity
    const packetValues = packetData.map(() => 1); // Count each packet as 1

    return {
      labels: packetTimes, // Packet IDs as X-axis (time)
      datasets: [
        {
          label: "Actual Traffic (Packets)",
          data: packetValues,
          borderColor: "purple",  // Purple color for packet data
          borderWidth: 2,
          fill: false,
        },
      ],
    };
  };

  return (
    <div className="chart-container">
      <h2>Actual Traffic (Packet Data)</h2>
      <Line data={prepareChartData()} />
    </div>
  );
}

export default PacketTrafficChart;
