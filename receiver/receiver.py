import time
import sys
import os
from pubsub import pub
from meshtastic.serial_interface import SerialInterface
from meshtastic import portnums_pb2

def find_meshtastic_port():
    """Find the Meshtastic device port based on the operating system"""
    if sys.platform == 'darwin':  # macOS
        # Common patterns for Meshtastic devices on macOS
        patterns = [
            '/dev/tty.usbserial*',
            '/dev/tty.SLAB_USBtoUART*',
            '/dev/tty.usbmodem*'
        ]
        for pattern in patterns:
            import glob
            ports = glob.glob(pattern)
            if ports:
                return ports[0]
    else:  # Linux/Ubuntu
        return '/dev/ttyUSB0'
    return None

def get_node_info(serial_port):
    print(f"Initializing SerialInterface to get node info on port {serial_port}...")
    local = SerialInterface(serial_port)
    node_info = local.nodes
    local.close()
    print("Node info retrieved.")
    return node_info

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
            print(f"{shortname}: {message}")
    except KeyError:
        pass  # Ignore KeyError silently
    except UnicodeDecodeError:
        pass  # Ignore UnicodeDecodeError silently

def main():
    # Find the correct port for the Meshtastic device
    serial_port = find_meshtastic_port()
    if not serial_port:
        print("Error: Could not find Meshtastic device. Please check your connection.")
        sys.exit(1)

    print(f"Using serial port: {serial_port}")

    # Retrieve and parse node information
    node_info = get_node_info(serial_port)
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
