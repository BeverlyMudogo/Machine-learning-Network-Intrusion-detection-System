# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class PacketCaptures(models.Model):
    protocol = models.IntegerField(db_column='Protocol', blank=True, null=True)  # Field name made lowercase.
    flow_duration = models.FloatField(db_column='Flow Duration', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    total_fwd_packets = models.IntegerField(db_column='Total Fwd Packets', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    total_backward_packets = models.IntegerField(db_column='Total Backward Packets', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    fwd_packets_length_total = models.FloatField(db_column='Fwd Packets Length Total', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    bwd_packets_length_total = models.FloatField(db_column='Bwd Packets Length Total', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    fwd_packet_length_max = models.FloatField(db_column='Fwd Packet Length Max', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    fwd_packet_length_min = models.FloatField(db_column='Fwd Packet Length Min', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    fwd_packet_length_mean = models.FloatField(db_column='Fwd Packet Length Mean', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    fwd_packet_length_std = models.FloatField(db_column='Fwd Packet Length Std', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    bwd_packet_length_max = models.FloatField(db_column='Bwd Packet Length Max', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    bwd_packet_length_min = models.FloatField(db_column='Bwd Packet Length Min', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    bwd_packet_length_mean = models.FloatField(db_column='Bwd Packet Length Mean', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    bwd_packet_length_std = models.FloatField(db_column='Bwd Packet Length Std', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    flow_bytes_s = models.FloatField(db_column='Flow Bytes/s', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    flow_packets_s = models.FloatField(db_column='Flow Packets/s', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    flow_iat_mean = models.FloatField(db_column='Flow IAT Mean', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    flow_iat_std = models.FloatField(db_column='Flow IAT Std', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    flow_iat_max = models.FloatField(db_column='Flow IAT Max', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    flow_iat_min = models.FloatField(db_column='Flow IAT Min', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    fwd_iat_total = models.FloatField(db_column='Fwd IAT Total', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    fwd_iat_mean = models.FloatField(db_column='Fwd IAT Mean', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    fwd_iat_std = models.FloatField(db_column='Fwd IAT Std', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    fwd_iat_max = models.FloatField(db_column='Fwd IAT Max', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    fwd_iat_min = models.FloatField(db_column='Fwd IAT Min', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    bwd_iat_total = models.FloatField(db_column='Bwd IAT Total', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    bwd_iat_mean = models.FloatField(db_column='Bwd IAT Mean', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    bwd_iat_std = models.FloatField(db_column='Bwd IAT Std', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    bwd_iat_max = models.FloatField(db_column='Bwd IAT Max', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    bwd_iat_min = models.FloatField(db_column='Bwd IAT Min', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    fwd_psh_flags = models.IntegerField(db_column='Fwd PSH Flags', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    bwd_psh_flags = models.IntegerField(db_column='Bwd PSH Flags', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    fwd_urg_flags = models.IntegerField(db_column='Fwd URG Flags', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    bwd_urg_flags = models.IntegerField(db_column='Bwd URG Flags', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    fwd_header_length = models.FloatField(db_column='Fwd Header Length', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    bwd_header_length = models.FloatField(db_column='Bwd Header Length', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    fwd_packets_s = models.FloatField(db_column='Fwd Packets/s', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    bwd_packets_s = models.FloatField(db_column='Bwd Packets/s', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    packet_length_min = models.FloatField(db_column='Packet Length Min', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    packet_length_max = models.FloatField(db_column='Packet Length Max', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    packet_length_mean = models.FloatField(db_column='Packet Length Mean', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    packet_length_std = models.FloatField(db_column='Packet Length Std', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    packet_length_variance = models.FloatField(db_column='Packet Length Variance', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    fin_flag_count = models.IntegerField(db_column='FIN Flag Count', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    syn_flag_count = models.IntegerField(db_column='SYN Flag Count', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    rst_flag_count = models.IntegerField(db_column='RST Flag Count', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    psh_flag_count = models.IntegerField(db_column='PSH Flag Count', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    ack_flag_count = models.IntegerField(db_column='ACK Flag Count', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    urg_flag_count = models.IntegerField(db_column='URG Flag Count', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cwe_flag_count = models.IntegerField(db_column='CWE Flag Count', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    ece_flag_count = models.IntegerField(db_column='ECE Flag Count', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    down_up_ratio = models.FloatField(db_column='Down/Up Ratio', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    avg_packet_size = models.FloatField(db_column='Avg Packet Size', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    avg_fwd_segment_size = models.FloatField(db_column='Avg Fwd Segment Size', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    avg_bwd_segment_size = models.FloatField(db_column='Avg Bwd Segment Size', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    fwd_avg_bytes_bulk = models.FloatField(db_column='Fwd Avg Bytes/Bulk', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    fwd_avg_packets_bulk = models.FloatField(db_column='Fwd Avg Packets/Bulk', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    fwd_avg_bulk_rate = models.FloatField(db_column='Fwd Avg Bulk Rate', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    bwd_avg_bytes_bulk = models.FloatField(db_column='Bwd Avg Bytes/Bulk', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    bwd_avg_packets_bulk = models.FloatField(db_column='Bwd Avg Packets/Bulk', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    bwd_avg_bulk_rate = models.FloatField(db_column='Bwd Avg Bulk Rate', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    subflow_fwd_packets = models.IntegerField(db_column='Subflow Fwd Packets', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    subflow_fwd_bytes = models.FloatField(db_column='Subflow Fwd Bytes', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    subflow_bwd_packets = models.IntegerField(db_column='Subflow Bwd Packets', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    subflow_bwd_bytes = models.FloatField(db_column='Subflow Bwd Bytes', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    init_fwd_win_bytes = models.FloatField(db_column='Init Fwd Win Bytes', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    init_bwd_win_bytes = models.FloatField(db_column='Init Bwd Win Bytes', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    fwd_act_data_packets = models.IntegerField(db_column='Fwd Act Data Packets', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    fwd_seg_size_min = models.FloatField(db_column='Fwd Seg Size Min', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    active_mean = models.FloatField(db_column='Active Mean', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    active_std = models.FloatField(db_column='Active Std', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    active_max = models.FloatField(db_column='Active Max', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    active_min = models.FloatField(db_column='Active Min', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    idle_mean = models.FloatField(db_column='Idle Mean', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    idle_std = models.FloatField(db_column='Idle Std', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    idle_max = models.FloatField(db_column='Idle Max', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    idle_min = models.FloatField(db_column='Idle Min', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    source_ip = models.GenericIPAddressField(db_column='Source IP', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    destination_ip = models.GenericIPAddressField(db_column='Destination IP', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    packet_id = models.BigAutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'packet_captures'


class Predictions(models.Model):
    packet_id = models.IntegerField(blank=True, null=True)
    prediction = models.IntegerField(blank=True, null=True)
    label = models.TextField(blank=True, null=True)
    prediction_timestamp = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'predictions'


class ProcessedPackets(models.Model):
    packet_id = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'processed_packets'


class ThreatAlerts(models.Model):
    alert_id = models.AutoField(primary_key=True)
    packet = models.ForeignKey(Predictions, models.DO_NOTHING, blank=True, null=True)
    threat_type = models.CharField(max_length=255, blank=True, null=True)
    severity = models.CharField(max_length=50, blank=True, null=True)
    alert_timestamp = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'threat_alerts'
