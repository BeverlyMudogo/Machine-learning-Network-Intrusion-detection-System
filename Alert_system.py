import psycopg2
import smtplib
from email.mime.text import MIMEText
from config import config

# Define severity levels
SEVERITY_MAPPING = {
    'Benign': 'Low',
    'DoS Hulk': 'High',
    'DDoS': 'Critical',
    'DoS GoldenEye': 'High',
    'FTP-Patator': 'Medium',
    'DoS slowloris': 'High',
    'DoS Slowhttptest': 'High',
    'SSH-Patator': 'Medium',
    'PortScan': 'Medium',
    'Web Attack – Brute Force': 'Critical',
    'Bot': 'High',
    'Web Attack – XSS': 'Medium',
    'Infiltration': 'Critical',
    'Web Attack – Sql Injection': 'Critical',
    'Heartbleed': 'Critical'
}

# Email Notification Function
def send_email_alert(threat_type, packet_id):
    sender_email = "nidscustodian@gmail.com"
    receiver_email = "beverlymudogo@zetech.ac.ke"
    subject = f"🚨 NIDS Alert: {threat_type} Detected!"
    body = f"A {threat_type} attack has been detected.\nPacket ID: {packet_id}\nPlease investigate immediately."

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = receiver_email

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login("nidscustodian@gmail.com", "cumtqtasakknhdiq")
            server.sendmail(sender_email, receiver_email, msg.as_string())
        print(f"Email alert sent for {threat_type} (Packet ID: {packet_id})")
    except Exception as e:
        print(f"Failed to send email alert: {e}")

# Connect to Database
def connect():
    try:
        params = config()
        conn = psycopg2.connect(**params)
        return conn
    except Exception as e:
        print(f"Database connection error: {e}")
        return None

# Monitor for Threats
def monitor_threats():
    conn = connect()
    if not conn:
        return

    cursor = conn.cursor()

    # Fetch new threats from predictions table
    cursor.execute("SELECT packet_id, prediction FROM predictions WHERE packet_id NOT IN (SELECT packet_id FROM threat_alerts)")
    new_threats = cursor.fetchall()

    for packet_id, prediction in new_threats:
        severity = SEVERITY_MAPPING.get(prediction, "Low")

        # Log the alert in the threat_alerts table
        cursor.execute(
            "INSERT INTO threat_alerts (packet_id, threat_type, severity) VALUES (%s, %s, %s)",
            (packet_id, prediction, severity)
        )

        # Send email alert for high-severity threats
        if severity in ["High", "Critical"]:
            send_email_alert(prediction, packet_id)

    # Commit changes and close connection
    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    monitor_threats()
