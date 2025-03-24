import psycopg2
import pandas as pd
import joblib
from config import config

# Load the trained model
NIDS_pipeline = joblib.load("/mnt/c/ML projects/ML-NIDS CIC-IDS2017/saved models/pipeline_v0.1.0.pkl")

# Define the label mapping (adjust this based on your model's output)
label_mapping = {
    0: 'Benign',  # Label 0 corresponds to "Benign"
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

# Establish the connection to the PostgreSQL database
def connect():
    connection = None
    try:
        params = config()
        print('Connecting to the PostgreSQL database....')
        connection = psycopg2.connect(**params)

        # Create a cursor
        cursor = connection.cursor()
        print('PostgreSQL database version: ')
        cursor.execute('SELECT version()')
        db_version = cursor.fetchone()
        print(db_version)
        
        return connection, cursor

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return None, None

# Define the query to fetch unprocessed packets using the `processed_packets` table
query = "SELECT * FROM packet_captures"

# Get the connection and cursor
conn, cursor = connect()

if conn is None or cursor is None:
    print("Failed to connect to the database.")
else:
    # Fetch the data from the database using the open connection
    df = pd.read_sql(query, conn)

    # Check the columns in the dataframe to confirm 'packet_id' is present
    print(df.columns)

    # Keep 'packet_id' and drop unnecessary columns that are not part of the model's training features
    df_model = df.drop(columns=["packet_id", "Source IP", "Destination IP"])

    # Make predictions using the loaded model
    try:
        df_model["prediction"] = NIDS_pipeline.predict(df_model)
        df_model["label"] = df_model["prediction"].map(label_mapping)  # Map predictions to labels
    except ValueError as e:
        print(f"Error making predictions: {e}")
        print(f"Input data columns: {df_model.columns}")
        # Handle the error (maybe by checking feature names and ensuring the columns match)
        exit(1)

    # Merge back to df
    df["prediction"] = df_model["prediction"]
    df["label"] = df_model["label"]


    # Insert the predictions and labels into the 'predictions' table
    for index, row in df.iterrows():
        # Use the original 'df' to access 'packet_id' and insert the data
        cursor.execute(
            "INSERT INTO predictions (packet_id, prediction, label, prediction_timestamp) VALUES (%s, %s, %s, CURRENT_TIMESTAMP)",
            (row["packet_id"], row["prediction"], row["label"])
        )

    # Commit the changes for inserting predictions
    conn.commit()

    # Close the cursor and the database connection
    cursor.close()
    conn.close()

if __name__ == '__main__':
    connect()
