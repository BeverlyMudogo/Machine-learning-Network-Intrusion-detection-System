CREATE TABLE predictions (
    id SERIAL PRIMARY KEY,
    packet_id INT,     -- This links to the packet id in the 'packets' table
    prediction INT,    -- Raw prediction (e.g., 0, 1, 2)
    label TEXT,         -- Human-readable label (e.g., "Normal", "Malicious")
    prediction_timestamp TIMESTAMP -- timestamp of prediction
);
