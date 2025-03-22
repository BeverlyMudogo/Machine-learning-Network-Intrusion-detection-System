
CREATE TABLE threat_alerts (
    alert_id SERIAL PRIMARY KEY,
    packet_id INTEGER REFERENCES predictions(id),
    threat_type VARCHAR(255),
    severity VARCHAR(50),
    alert_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
