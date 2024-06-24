import csv
from scapy.all import rdpcap, IP, TCP, UDP
from collections import defaultdict
import time

# Function to create a normalized flow key for bidirectional flows
def get_flow_key(packet):
    if TCP in packet:
        proto = 'TCP'
        src_port = packet[TCP].sport
        dst_port = packet[TCP].dport
    elif UDP in packet:
        proto = 'UDP'
        src_port = packet[UDP].sport
        dst_port = packet[UDP].dport
    else:
        return None
    
    src_ip = packet[IP].src
    dst_ip = packet[IP].dst

    # Normalize the 5-tuple to handle bidirectional flows
    if (src_ip, src_port) < (dst_ip, dst_port):
        return (src_ip, dst_ip, src_port, dst_port, proto)
    else:
        return (dst_ip, src_ip, dst_port, src_port, proto)

# Load the pcap file
pcap_file = 'teste.pcap'
packets = rdpcap(pcap_file)

flows = defaultdict(lambda: {'start_time': None, 'end_time': None, 'total_bytes': 0, 'num_packets': 0})
inactive_timeout = 10000  # 10 seconds inactivity timeout

# Iterate through the packets
for packet in packets:
    if IP in packet:
        flow_key = get_flow_key(packet)
        if flow_key is None:
            continue
        
        current_time = packet.time
        
        if flows[flow_key]['start_time'] is None:
            # Start a new flow
            flows[flow_key]['start_time'] = current_time
            flows[flow_key]['end_time'] = current_time
            flows[flow_key]['total_bytes'] = len(packet)
            flows[flow_key]['num_packets'] = 1
        else:
            last_packet_time = flows[flow_key]['end_time']
            if TCP in packet and packet[TCP].flags & 0x01:  # Check if the FIN flag is set
                # End the TCP flow with FIN flag
                flows[flow_key]['end_time'] = current_time
            elif current_time - last_packet_time > inactive_timeout:
                # End the flow due to inactivity
                flows[flow_key]['end_time'] = current_time
                # Start a new flow
                flows[flow_key]['start_time'] = current_time
                flows[flow_key]['end_time'] = current_time
                flows[flow_key]['total_bytes'] = len(packet)
                flows[flow_key]['num_packets'] = 1
            else:
                # Continue the flow
                flows[flow_key]['end_time'] = current_time
                flows[flow_key]['total_bytes'] += len(packet)
                flows[flow_key]['num_packets'] += 1

# Collect flow information to save to CSV
flow_data = []
for flow_key, flow_info in flows.items():
    src_ip, dst_ip, src_port, dst_port, proto = flow_key
    duration = (flow_info['end_time'] - flow_info['start_time'])
    num_bytes = flow_info['total_bytes']
    num_packets = flow_info['num_packets']
    flow_data.append([src_ip, dst_ip, src_port, dst_port, proto, duration, num_bytes, num_packets])

# Save to CSV file
csv_file = 'network_flows.csv'
with open(csv_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Source IP', 'Destination IP', 'Source Port', 'Destination Port', 'Protocol', 'Duration (ms)', 'Number of Bytes', 'Number of Packets'])
    writer.writerows(flow_data)

print(f'Flow information saved to {csv_file}')
