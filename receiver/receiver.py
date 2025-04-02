import time
import sys
import serial.tools.list_ports
from pubsub import pub
from meshtastic.serial_interface import SerialInterface
from meshtastic import portnums_pb2
import csv

def find_usb_serial_port():
    print("Searching for USB serial devices...")
    ports = list(serial.tools.list_ports.comports())
    for port in ports:
        print(f"Found device: {port.device} - {port.description}")
        if "CP210x" in port.description:
            print(f"Using port: {port.device}")
            return port.device
    print("No USB serial device found with the specified description.")
    return None

def get_node_info(serial_port):
    print("Initializing SerialInterface to get node info...")
    try:
        local = SerialInterface(serial_port)  # Increase timeout to 60 seconds
        node_info = local.nodes
        local.close()
        print("Node info retrieved.")
        return node_info
    except Exception as e:
        print(f"Failed to initialize SerialInterface: {e}")
        return None

def parse_node_info(node_info):
    print("Parsing node info...")
    nodes = []
    for node_id, node in node_info.items():
        nodes.append({
            'num': node_id,
            'user': {
                'shortName': node.get('user', {}).get('shortName', 'Unknown')
            }
        })
    print("Node info parsed.")
    return nodes

def on_receive(packet, interface, node_list):
    try:
        if packet['decoded']['portnum'] == 'TEXT_MESSAGE_APP':
            message = packet['decoded']['payload'].decode('utf-8')
            fromnum = packet['fromId']
            shortname = next((node['user']['shortName'] for node in node_list if node['num'] == fromnum), 'Unknown')
            rows = message.splitlines()  # Split the message into lines
            with open('radioTest.csv', 'a', newline='') as csvfile:  # Open in append mode ('a')
                rowWriter = csv.writer(csvfile, delimiter=',')
                i = 1
                
                for row in rows:
                    print("Row #", i, ": ", row)
                    i = i + 1
                    data = row.strip().split(',')  # Split each line into columns
                    rowWriter.writerow(data)  # Write the row to the CSV file
            print(f"{shortname}: {message}")
    except KeyError:
        pass  # Ignore KeyError silently
    except UnicodeDecodeError:
        pass  # Ignore UnicodeDecodeError silently

def main():
    serial_port = find_usb_serial_port()
    if not serial_port:
        print("Exiting program.")
        return

    print(f"Using serial port: {serial_port}")

    # Retrieve and parse node information
    node_info = get_node_info(serial_port)
    if not node_info:
        print("Failed to get node info.")
        return
    node_list = parse_node_info(node_info)

    # Print node list for debugging
    print("Node List:")
    for node in node_list:
        print(node)

    # Subscribe the callback function to message reception
    def on_receive_wrapper(packet, interface):
        on_receive(packet, interface, node_list)

    pub.subscribe(on_receive_wrapper, "meshtastic.receive")
    print("Subscribed to meshtastic.receive")

    # Set up the SerialInterface for message listening
    local = SerialInterface(serial_port)
    print("SerialInterface setup for listening.")

    # Keep the script running to listen for messages
    try:
        while True:
            sys.stdout.flush()
            time.sleep(1)  # Sleep to reduce CPU usage
    except KeyboardInterrupt:
        print("Script terminated by user")
        local.close()

if __name__ == "__main__":
    main()