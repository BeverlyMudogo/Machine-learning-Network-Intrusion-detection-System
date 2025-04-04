from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils.timezone import now
import subprocess  # To trigger external scripts
import threading  # To run it in the background
import os

# Start packet capture API
def start_packet_capture():
    # Get the directory of the current script
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Move up to the project root folder
    project_root = os.path.abspath(os.path.join(base_dir, "..", ".."))
    
    # Construct absolute paths to the scripts
    config_script = os.path.join( project_root, "config.py")
    capture_script = os.path.join( project_root, "packet_capture_engine.py")

    # Replace this with your actual packet capture command
    subprocess.run(["python", config_script])
    subprocess.run(["python", capture_script])

@api_view(['POST'])
def start_capture(request):
    threading.Thread(target=start_packet_capture).start()
    return Response({"message": "Packet capture started"}, status=200)

# Trigger prediction script
def start_prediction():
    # Get the directory of the current script
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Move up to the project root folder
    project_root = os.path.abspath(os.path.join(base_dir, "..", ".."))
    
    prediction_script = os.path.join( project_root, "modelconnectdb.py")
    
    # prediction script
    subprocess.run(["python", prediction_script])

@api_view(['POST'])
def start_prediction_trigger(request):
    threading.Thread(target=start_prediction).start()
    return Response({"message": "Prediction process started"}, status=200)

# Fetch API predictions
from myapp.models import Predictions  #  model import 
from rest_framework import status

@api_view(['GET'])
def get_predictions(request):
    predictions = Predictions.objects.all().order_by('-prediction_timestamp')[:50]
    data = [{"id": p.packet_id, "prediction": p.prediction, "Label": p.label, "timestamp": p.prediction_timestamp} for p in predictions]
    return Response(data, status=status.HTTP_200_OK)

# Send alerts
from myapp.models import ThreatAlerts  # model import
from django.core.mail import send_mail

# trigger alert logging to threat_alerts db
def send_alertnote():
    # Get the directory of the current script
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Move up to the project root folder
    project_root = os.path.abspath(os.path.join(base_dir, "..", ".."))
    
    alert_script = os.path.join( project_root, "Alert_system.py")

    subprocess.run(['python', alert_script])
    
@api_view(['POST'])
def send_alert(request):
    threading.Thread(target=send_alertnote).start()
    return Response({'message': 'Alert sent!'}, status=200)

#fetch captured packets
from myapp.models import PacketCaptures  #  model import 
from rest_framework import status

@api_view(['GET'])
def get_packets(request):
    packetcaptures = PacketCaptures.objects.all().order_by('-packet_id')[:30]
    data = [{"id": p.packet_id, "SourceIP": p.source_ip, "DestinationIp": p.destination_ip, "protocol": p.protocol} for p in packetcaptures]
    return Response(data, status=status.HTTP_200_OK)