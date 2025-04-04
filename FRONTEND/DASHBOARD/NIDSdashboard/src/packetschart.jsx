import React, { useEffect, useState } from "react";
import axios from "axios";

const PacketTrafficChart = () => {
  const [data, setData] = useState([]);

  const apiUrl = "http://127.0.0.1:8000"; 
  

  // Fetch predictions from the API
  useEffect(() => {
    axios
      .get(`${apiUrl}/api/get_packets`)
      .then((response) => {
        setData(response.data);
      })
      .catch((error) => {
        console.error("Error fetching packets:", error);
      });
  }, []);

  return (
    <div className="glass-table-container">
      <h2 style={{ textAlign: "center", color: "#7a7f85", marginBottom: "20px" }}>Packet captures</h2>
      <table className="glass-table" border="1" cellPadding="8">
        <thead>
          <tr>
            <th>ID</th>
            <th>Source Ip</th>
            <th>Destination IP</th>
            <th>Protocol</th>
          </tr>
        </thead>
        <tbody>
          {data.length > 0 ? (
            data.map((packetcaptures) => (
              <tr key={packetcaptures.id}>
                <td>{packetcaptures.id}</td>
                <td>{packetcaptures.SourceIP}</td>
                <td>{packetcaptures.DestinationIp}</td>
                <td>{packetcaptures.protocol}</td>
              </tr>
            ))
          ) : (
            <tr>
              <td colSpan={4} style={{ textAlign: "center" }}>
                No Data Available
              </td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
};

export default PacketTrafficChart;
