from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils.timezone import now
import subprocess  # To trigger external scripts
import threading  # To run it in the background

# Start packet capture API
def start_packet_capture():
    # Replace this with your actual packet capture command
    subprocess.run(["python", "../config.py"])
    subprocess.run(["python", "../packet_capture_engine.py"])

@api_view(['POST'])
def start_capture(request):
    threading.Thread(target=start_packet_capture).start()
    return Response({"message": "Packet capture started"}, status=200)

# Trigger prediction script
def start_prediction():
    # prediction script
    subprocess.run(["python", "../modelconnectdb.py"])

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
    subprocess.run(['python', '../Alert_system.py'])
    
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
    data = [{"id": p.packet_id, "source ip": p.source_ip, "destination ip": p.destination_ip, "protocol": p.protocol} for p in packetcaptures]
    return Response(data, status=status.HTTP_200_OK)