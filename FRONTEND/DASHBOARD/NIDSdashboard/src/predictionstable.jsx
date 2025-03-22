import React, { useEffect, useState } from "react";
import axios from "axios";

const PredictionsTable = () => {
  const [data, setData] = useState([]);

  // Fetch predictions from the API
  useEffect(() => {
    axios
      .get("http://127.0.0.1:8000/api/get_predictions/")
      .then((response) => {
        setData(response.data);
      })
      .catch((error) => {
        console.error("Error fetching predictions:", error);
      });
  }, []);

  return (
    <div className="glass-table-container">
      <h2 style={{ textAlign: "center", color: "#7a7f85", marginBottom: "20px" }}>Predictions</h2>
      <table className="glass-table" border="1" cellPadding="8">
        <thead>
          <tr>
            <th>ID</th>
            <th>Prediction</th>
            <th>Label</th>
            <th>Timestamp</th>
          </tr>
        </thead>
        <tbody>
          {data.length > 0 ? (
            data.map((prediction) => (
              <tr key={prediction.id}>
                <td>{prediction.id}</td>
                <td>{prediction.prediction}</td>
                <td>{prediction.Label}</td>
                <td>{prediction.timestamp}</td>
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

export default PredictionsTable;
