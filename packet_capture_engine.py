import pyshark
import pandas as pd
import time
import numpy as np
from collections import defaultdict
import psycopg2
from config import config

# Connect to the PostgreSQL database
def connect():
    connection = None
    columns = None
    try:
        params = config()
        print('Connecting to the postgreSQL database....')
        connection = psycopg2.connect(**params)

        # Create a cursor
        crsr = connection.cursor()
        print('PostgreSQL database version: ')
        crsr.execute("SELECT version()")
        db_version = crsr.fetchone()
        print(db_version)
        
        # Fetch the column names from the 'packet_captures' table
        crsr.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'packet_captures'")
        columns = crsr.fetchall()
        crsr.close()

        return connection, columns
        
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        
    return connection, columns







class PacketCaptureEngine:
    def __init__(self, interface='Wi-Fi', capture_duration=30):
        self.interface = interface
        self.capture_duration = capture_duration
        self.flow_features = defaultdict(lambda: defaultdict(float))
        self.last_seen = {}
        self.flow_packet_times = defaultdict(list)
        
        self.flow_states = defaultdict(lambda: {'state': 'idle', 'start_time': None, 'active_durations': [], 'idle_durations': []})
        
        self.feature_keys = [
            'Protocol', 'Flow Duration', 'Total Fwd Packets', 'Total Backward Packets', 'Fwd Packets Length Total',
            'Bwd Packets Length Total', 'Fwd Packet Length Max', 'Fwd Packet Length Min', 'Fwd Packet Length Mean',
            'Fwd Packet Length Std', 'Bwd Packet Length Max', 'Bwd Packet Length Min', 'Bwd Packet Length Mean',
            'Bwd Packet Length Std', 'Flow Bytes/s', 'Flow Packets/s', 'Flow IAT Mean', 'Flow IAT Std', 'Flow IAT Max',
            'Flow IAT Min', 'Fwd IAT Total', 'Fwd IAT Mean', 'Fwd IAT Std', 'Fwd IAT Max', 'Fwd IAT Min',
            'Bwd IAT Total', 'Bwd IAT Mean', 'Bwd IAT Std', 'Bwd IAT Max', 'Bwd IAT Min', 'Fwd PSH Flags',
            'Bwd PSH Flags', 'Fwd URG Flags', 'Bwd URG Flags', 'Fwd Header Length', 'Bwd Header Length',
            'Fwd Packets/s', 'Bwd Packets/s', 'Packet Length Min', 'Packet Length Max', 'Packet Length Mean',
            'Packet Length Std', 'Packet Length Variance', 'FIN Flag Count', 'SYN Flag Count', 'RST Flag Count',
            'PSH Flag Count', 'ACK Flag Count', 'URG Flag Count', 'CWE Flag Count', 'ECE Flag Count', 'Down/Up Ratio',
            'Avg Packet Size', 'Avg Fwd Segment Size', 'Avg Bwd Segment Size', 'Fwd Avg Bytes/Bulk',
            'Fwd Avg Packets/Bulk', 'Fwd Avg Bulk Rate', 'Bwd Avg Bytes/Bulk', 'Bwd Avg Packets/Bulk',
            'Bwd Avg Bulk Rate', 'Subflow Fwd Packets', 'Subflow Fwd Bytes', 'Subflow Bwd Packets',
            'Subflow Bwd Bytes', 'Init Fwd Win Bytes', 'Init Bwd Win Bytes', 'Fwd Act Data Packets',
            'Fwd Seg Size Min', 'Active Mean', 'Active Std', 'Active Max', 'Active Min', 'Idle Mean', 'Idle Std',
            'Idle Max', 'Idle Min'
        ]
    
    def extract_features(self, packet):
        try:
            flow_id = f"{packet.ip.src}-{packet.ip.dst}-{packet.transport_layer}-{packet[packet.transport_layer].srcport}-{packet[packet.transport_layer].dstport}"
            timestamp = float(packet.sniff_time.timestamp())
            length = int(packet.length) if hasattr(packet, 'length') else 0
            
            for key in self.feature_keys:
                self.flow_features[flow_id].setdefault(key, 0)
            
            
             # Add source_ip, and destination_ip
            
            self.flow_features[flow_id]['Source IP'] = packet.ip.src
            self.flow_features[flow_id]['Destination IP'] = packet.ip.dst
        
            protocol_map = {'TCP': 6, 'UDP': 17, 'ICMP': 1}
            self.flow_features[flow_id]['Protocol'] = protocol_map.get(packet.transport_layer, 0)
            self.flow_features[flow_id]['Flow Duration'] = timestamp - self.flow_features[flow_id].get('Flow Start Time', timestamp)
            self.flow_features[flow_id]['Flow Start Time'] = min(self.flow_features[flow_id].get('Flow Start Time', timestamp), timestamp)
            
            # Packet classification: Active vs Idle
            is_idle = self.detect_idle(packet, length)

            # Track active/idle periods
            self.track_flow_state(flow_id, timestamp, is_idle)
            
            if packet.ip.src:
                self.flow_features[flow_id]['Total Fwd Packets'] += 1
                self.flow_features[flow_id]['Fwd Packets Length Total'] += length
                
                self.flow_features[flow_id]['Fwd Packet Length Max'] = max(self.flow_features[flow_id]['Fwd Packet Length Max'], length)
                self.flow_features[flow_id]['Fwd Packet Length Min'] = min(self.flow_features[flow_id]['Fwd Packet Length Min'], length) if self.flow_features[flow_id]['Fwd Packet Length Min'] else length
                
                self.flow_features[flow_id].setdefault('Fwd Packet Lengths', []).append(length)
                
                if len(self.flow_features[flow_id]['Fwd Packet Lengths']) > 1:
                    self.flow_features[flow_id]['Fwd Packet Length Mean'] = np.mean(self.flow_features[flow_id]['Fwd Packet Lengths'])
                    self.flow_features[flow_id]['Fwd Packet Length Std'] = np.std(self.flow_features[flow_id]['Fwd Packet Lengths'])
                
            if packet.ip.dst:
                self.flow_features[flow_id]['Total Backward Packets'] += 1
                self.flow_features[flow_id]['Bwd Packets Length Total'] += length
                
                self.flow_features[flow_id]['Bwd Packet Length Max'] = max(self.flow_features[flow_id]['Bwd Packet Length Max'], length)
                self.flow_features[flow_id]['Bwd Packet Length Min'] = min(self.flow_features[flow_id]['Bwd Packet Length Min'], length) if self.flow_features[flow_id]['Bwd Packet Length Min'] else length
                
                self.flow_features[flow_id].setdefault('Bwd Packet Lengths', []).append(length)
                
                if len(self.flow_features[flow_id]['Bwd Packet Lengths']) > 1:
                    self.flow_features[flow_id]['Bwd Packet Length Mean'] = np.mean(self.flow_features[flow_id]['Bwd Packet Lengths'])
                    self.flow_features[flow_id]['Bwd Packet Length Std'] = np.std(self.flow_features[flow_id]['Bwd Packet Lengths'])
            
            self.flow_packet_times[flow_id].append(timestamp)
            
            if self.flow_features[flow_id]['Flow Duration'] > 0:
                self.flow_features[flow_id]['Flow Bytes/s'] = (self.flow_features[flow_id]['Fwd Packets Length Total'] + self.flow_features[flow_id]['Bwd Packets Length Total']) / self.flow_features[flow_id]['Flow Duration']
                self.flow_features[flow_id]['Flow Packets/s'] = (self.flow_features[flow_id]['Total Fwd Packets'] + self.flow_features[flow_id]['Total Backward Packets']) / self.flow_features[flow_id]['Flow Duration']
            
            if flow_id in self.last_seen:
                iat = timestamp - self.last_seen[flow_id]
                self.flow_features[flow_id].setdefault('Flow IATs', []).append(iat)
                
                self.flow_features[flow_id]['Flow IAT Total'] += iat
                self.flow_features[flow_id]['Flow IAT Mean'] = np.mean(self.flow_features[flow_id]['Flow IATs'])
                self.flow_features[flow_id]['Flow IAT Std'] = np.std(self.flow_features[flow_id]['Flow IATs'])
                self.flow_features[flow_id]['Flow IAT Max'] = max(self.flow_features[flow_id]['Flow IATs'])
                self.flow_features[flow_id]['Flow IAT Min'] = min(self.flow_features[flow_id]['Flow IATs'])
                
                self.flow_features[flow_id].setdefault('Fwd IATs', []).append(iat)
                self.flow_features[flow_id].setdefault('Bwd IATs', []).append(iat)
                
                self.flow_features[flow_id]['Fwd IAT Total'] = sum(self.flow_features[flow_id]['Fwd IATs'])
                self.flow_features[flow_id]['Fwd IAT Mean'] = np.mean(self.flow_features[flow_id]['Fwd IATs'])
                self.flow_features[flow_id]['Fwd IAT Std'] = np.std(self.flow_features[flow_id]['Fwd IATs'])
                self.flow_features[flow_id]['Fwd IAT Max'] = max(self.flow_features[flow_id]['Fwd IATs'])
                self.flow_features[flow_id]['Fwd IAT Min'] = min(self.flow_features[flow_id]['Fwd IATs'])
                
                self.flow_features[flow_id]['Bwd IAT Total'] = sum(self.flow_features[flow_id]['Bwd IATs'])
                self.flow_features[flow_id]['Bwd IAT Mean'] = np.mean(self.flow_features[flow_id]['Bwd IATs'])
                self.flow_features[flow_id]['Bwd IAT Std'] = np.std(self.flow_features[flow_id]['Bwd IATs'])
                self.flow_features[flow_id]['Bwd IAT Max'] = max(self.flow_features[flow_id]['Bwd IATs'])
                self.flow_features[flow_id]['Bwd IAT Min'] = min(self.flow_features[flow_id]['Bwd IATs'])
            
                
            
            
            
            self.flow_features[flow_id]['Avg Packet Size'] = (self.flow_features[flow_id]['Fwd Packets Length Total'] + self.flow_features[flow_id]['Bwd Packets Length Total']) / max((self.flow_features[flow_id]['Total Fwd Packets'] + self.flow_features[flow_id]['Total Backward Packets']), 1)
            
            if hasattr(packet, 'tcp'):
                self.flow_features[flow_id]['Init Fwd Win Bytes'] += int(packet.tcp.window_size)
                self.flow_features[flow_id]['Init Bwd Win Bytes'] += int(packet.tcp.window_size)
                
                
                flags = int(packet.tcp.flags, 16)
                self.flow_features[flow_id]['FIN Flag Count'] += (flags & 0x01) >> 0
                self.flow_features[flow_id]['SYN Flag Count'] += (flags & 0x02) >> 1
                self.flow_features[flow_id]['RST Flag Count'] += (flags & 0x04) >> 2
                self.flow_features[flow_id]['PSH Flag Count'] += (flags & 0x08) >> 3
                self.flow_features[flow_id]['ACK Flag Count'] += (flags & 0x10) >> 4
                self.flow_features[flow_id]['URG Flag Count'] += (flags & 0x20) >> 5
                self.flow_features[flow_id]['CWE Flag Count'] += (flags & 0x40) >> 6
                self.flow_features[flow_id]['ECE Flag Count'] += (flags & 0x80) >> 7
                
                
                self.flow_features[flow_id]['Fwd PSH Flags'] += (flags & 0x08) >> 3
                self.flow_features[flow_id]['Bwd PSH Flags'] += (flags & 0x08) >> 3
                self.flow_features[flow_id]['Fwd URG Flags'] += (flags & 0x20) >> 5
                self.flow_features[flow_id]['Bwd URG Flags'] += (flags & 0x20) >> 5
                
                
            # Capture TCP, UDP, and ICMP Header Length
            if hasattr(packet, 'tcp'):
                header_length = int(packet.tcp.hdr_len) * 4  # Convert to bytes
                if packet.ip.src:
                    self.flow_features[flow_id]['Fwd Header Length'] += header_length
                else:
                    self.flow_features[flow_id]['Bwd Header Length'] += header_length
                
            elif hasattr(packet, 'udp'):
                header_length = 8  # UDP header is always 8 bytes
                if packet.ip.src:
                    self.flow_features[flow_id]['Fwd Header Length'] += header_length
                else:
                    self.flow_features[flow_id]['Bwd Header Length'] += header_length
            
            elif hasattr(packet, 'icmp'):
                    header_length = 8  # Common ICMP header size
                    if packet.ip.src:
                        self.flow_features[flow_id]['Fwd Header Length'] += header_length
                    else:
                        self.flow_features[flow_id]['Bwd Header Length'] += header_length

            # Compute Fwd and Bwd Packets per Second
            flow_duration = self.flow_features[flow_id]['Flow Duration']
            if flow_duration > 0:
                self.flow_features[flow_id]['Fwd Packets/s'] = self.flow_features[flow_id]['Total Fwd Packets'] / flow_duration
                self.flow_features[flow_id]['Bwd Packets/s'] = self.flow_features[flow_id]['Total Backward Packets'] / flow_duration

                
            
                
             
            self.last_seen[flow_id] = timestamp
            
        except AttributeError:
            pass # Ignore packets without IP layer
       
    def detect_idle(self, packet, length):
        if hasattr(packet, 'tcp'):
            flags = int(packet.tcp.flags, 16)
            if length == 0 or (flags & (0x01 | 0x02 | 0x04 | 0x10)):  # FIN, SYN, RST, ACK
                return True
        return False
    
    def track_flow_state(self, flow_id, timestamp, is_idle):
        state = self.flow_states[flow_id]
        if state['state'] == 'idle' and not is_idle:
            state['idle_durations'].append(timestamp - state['start_time'] if state['start_time'] else 0)
            state['start_time'] = timestamp
            state['state'] = 'active'
        elif state['state'] == 'active' and is_idle:
            state['active_durations'].append(timestamp - state['start_time'] if state['start_time'] else 0)
            state['start_time'] = timestamp
            state['state'] = 'idle'
            
            
    def finalize_features(self):
        for flow_id, state in self.flow_states.items():
            self.flow_features[flow_id].update(self.calculate_stats(state['active_durations'], "Active"))
            self.flow_features[flow_id].update(self.calculate_stats(state['idle_durations'], "Idle"))
            
    def calculate_stats(self, durations, prefix):
        return {
            f'{prefix} Mean': np.mean(durations) if durations else 0,
            f'{prefix} Std': np.std(durations) if durations else 0,
            f'{prefix} Max': max(durations) if durations else 0,
            f'{prefix} Min': min(durations) if durations else 0
        } 
        
    
    
    # Insert flow data into PostgreSQL
    def insert_flow_data(self, connection, flow_data, columns):
        try:
            cursor = connection.cursor()
            
            # Example columns in flow_data (assuming the keys in flow_data correspond to your table columns)
            columns_in_flow_data = flow_data.keys()
            
            # Extract column names as a list
            expected_table_columns = [col[0] for col in columns]

            # Ensure only valid columns from flow_data exist in the insert query
            valid_columns = [col for col in columns_in_flow_data if col in expected_table_columns]
            
            # Ensure 'Timestamp', 'Source IP', and 'Destination IP' are always inserted
            required_columns = [ 'Source IP', 'Destination IP']
            valid_columns.extend([col for col in required_columns if col not in valid_columns])

            # Construct the SQL query dynamically based on the valid columns
            columns_str = ', '.join([f'"{col}"' for col in valid_columns])
            placeholders = ', '.join(['%s'] * len(valid_columns))
            
             
            
            insert_query = f"""
            
            INSERT INTO packet_captures ({columns_str})
            VALUES ({placeholders})


            """
           
            
            # Convert flow_data into a tuple that matches the table columns
            # Convert flow_data to a tuple with only the valid columns
            flow_data_tuple = tuple(flow_data[col] for col in valid_columns)


            
            # Debugging: Check the length of the tuple and placeholders
            print(f"Number of placeholders: {len(insert_query.split('%s')) - 1}")
            print(f"Number of values in flow_data_tuple: {len(flow_data_tuple)}")

            
            # execute the insert queries
            cursor.execute(insert_query, flow_data_tuple)
            connection.commit()
            cursor.close()
            print(f"Flow data inserted successfully.")
            
        except (Exception, psycopg2.DatabaseError) as error:
            print(f"Error inserting data: {error}")



    def capture_packets(self):
        cap = pyshark.LiveCapture(interface=self.interface)
        start_time = time.time()
        connection, columns = connect()  # Connect to the database and fetch columns
        

        
        for packet in cap.sniff_continuously():
            if time.time() - start_time > self.capture_duration:
                break
            
            self.extract_features(packet)    

                     
        self.finalize_features()
        cap.close()
        
        # Insert flow data into the PostgreSQL database
        for flow_id, flow_data in self.flow_features.items():
            self.insert_flow_data(connection, flow_data, columns)
            
            
        df = pd.DataFrame.from_dict(self.flow_features, orient='index')
        df = df[self.feature_keys]  # Ensure correct column order
        
        return df
       
if __name__ == "__main__":
    engine = PacketCaptureEngine(interface='Wi-Fi', capture_duration=30)
    df = engine.capture_packets()
    print(df)
    
