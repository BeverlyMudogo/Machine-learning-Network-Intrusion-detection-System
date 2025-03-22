import streamlit as st
import pandas as pd
import joblib

# Load the saved pipeline
pipeline = joblib.load("saved models/pipeline_v0.1.0.pkl")

# Define label mapping
label_mapping = {
    0: 'Benign',
    1: 'DoS Hulk',
    2: 'DDoS',
    3: 'DoS GoldenEye',
    4: 'FTP-Patator',
    5: 'DoS slowloris',
    6: 'DoS Slowhttptest',
    7: 'SSH-Patator',
    8: 'PortScan',
    9: 'Web Attack – Brute Force',
    10: 'Bot',
    11: 'Web Attack – XSS',
    12: 'Infiltration',
    13: 'Web Attack – Sql Injection',
    14: 'Heartbleed'
}

st.title("Network Intrusion Detection System")
st.write("Upload a CSV file containing network traffic data for real-time anomaly detection.")

# File uploader
uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

if uploaded_file is not None:
    # Read the CSV file
    df = pd.read_csv(uploaded_file)
    
    st.write("### Uploaded Data Preview:")
    st.write(df.head(10))
    
    # Make predictions
    predictions = pipeline.predict(df)
    
    # Convert predictions to labels
    labeled_predictions = [label_mapping[pred] for pred in predictions]
    
    # Convert predictions to DataFrame
    results_df = pd.DataFrame({"Prediction": labeled_predictions})
    
    st.write("### Prediction Results:")
    st.write(results_df.head(10))
    
    # Allow users to download results
    csv = results_df.to_csv(index=False).encode("utf-8")
    st.download_button("Download Predictions", data=csv, file_name="predictions.csv", mime="text/csv")
