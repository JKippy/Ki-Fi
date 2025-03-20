import time
import sys
import os
import serial
import signal
import subprocess
from datetime import datetime
from pubsub import pub
from meshtastic.serial_interface import SerialInterface
from meshtastic import portnums_pb2

# Global variable to store the SerialInterface instance
local = None
LOG_FILE = "meshtastic_messages.txt"

def signal_handler(signum, frame):
    """Handle Ctrl+C gracefully"""
    print("\nReceived signal to terminate. Cleaning up...")
    if local:
        try:
            local.close()
        except:
            pass
    sys.exit(0)

def log_message(message, sender):
    """Log message to file with timestamp"""
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {sender}: {message}\n"
        
        with open(LOG_FILE, "a", encoding='utf-8') as f:
            f.write(log_entry)
        print(f"Message logged to {LOG_FILE}")
    except Exception as e:
        print(f"Error logging message: {e}")

def check_usb_device(show_info=False):
    """Check USB device status"""
    try:
        # Check USB devices
        result = subprocess.run(['system_profiler', 'SPUSBDataType'], capture_output=True, text=True)
        if show_info:
            print("USB Devices:")
            print(result.stdout)
        
        # Check serial ports
        result = subprocess.run(['ls', '-l', '/dev/tty.*'], capture_output=True, text=True)
        if show_info:
            print("\nSerial Ports:")
            print(result.stdout)
        
        # Check if any process is using the port
        result = subprocess.run(['lsof', '|', 'grep', 'usbserial'], shell=True, capture_output=True, text=True)
        if show_info:
            print("\nProcesses using serial port:")
            print(result.stdout)
        
        return True
    except Exception as e:
        print(f"Error checking USB device: {e}")
        return False

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

def test_serial_connection(port):
    """Test basic serial connection with detailed debugging"""
    print(f"\nTesting serial connection to {port}...")
    try:
        # Try to open the port with different baud rates
        baud_rates = [115200, 57600, 38400, 19200, 9600]
        for baud in baud_rates:
            print(f"Trying baud rate {baud}...")
            try:
                with serial.Serial(port, baudrate=baud, timeout=1) as ser:
                    print(f"Successfully opened port at {baud} baud")
                    # Try to read any data
                    if ser.in_waiting:
                        data = ser.read(ser.in_waiting)
                        print(f"Found {len(data)} bytes of data")
                    return True
            except serial.SerialException as e:
                print(f"Failed at {baud} baud: {e}")
                continue
        return False
    except Exception as e:
        print(f"Error testing serial connection: {e}")
        return False

def create_serial_interface(port, timeout=5):
    """Create a SerialInterface with a timeout"""
    print(f"Creating SerialInterface with {timeout} second timeout...")
    start_time = time.time()
    
    try:
        # First try to open the port directly with specific settings
        ser = serial.Serial(
            port=port,
            baudrate=115200,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            timeout=1,
            xonxoff=False,
            rtscts=False,
            dsrdtr=False
        )
        print("Basic serial port opened successfully")
        
        # Try to create the interface
        interface = SerialInterface(port)
        print("SerialInterface created successfully")
        return interface
    except Exception as e:
        print(f"Error creating SerialInterface: {e}")
        if 'ser' in locals():
            try:
                ser.close()
            except:
                pass
        return None

def get_node_info(serial_port):
    print(f"\nInitializing SerialInterface to get node info on port {serial_port}...")
    try:
        # First test the serial connection
        if not test_serial_connection(serial_port):
            print("Failed to establish basic serial connection")
            return None

        # Try to create the interface with a timeout
        interface = create_serial_interface(serial_port)
        if not interface:
            print("Failed to create SerialInterface")
            return None

        try:
            print("Attempting to get nodes...")
            node_info = interface.nodes
            print("Nodes retrieved successfully")
            return node_info
        finally:
            print("Closing interface...")
            interface.close()
            print("Interface closed successfully")
            
    except Exception as e:
        print(f"Error getting node info: {e}")
        print(f"Error type: {type(e).__name__}")
        print(f"Error details: {e.__dict__ if hasattr(e, '__dict__') else 'No details available'}")
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
            print(f"{shortname}: {message}")
            # Log the message to file
            log_message(message, shortname)
    except KeyError:
        pass  # Ignore KeyError silently
    except UnicodeDecodeError:
        pass  # Ignore UnicodeDecodeError silently

def main():
    global local
    
    # Set up signal handler for Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Check USB device status first (without showing info)
    if not check_usb_device(show_info=False):
        print("Warning: Could not check USB device status")
        # If there's an issue, show the device info for debugging
        check_usb_device(show_info=True)
    
    # Find the correct port for the Meshtastic device
    serial_port = find_meshtastic_port()
    if not serial_port:
        print("Error: Could not find Meshtastic device. Please check your connection.")
        sys.exit(1)

    print(f"Using serial port: {serial_port}")

    # Retrieve and parse node information
    node_info = get_node_info(serial_port)
    if not node_info:
        print("Error: Could not get node information. Please check device connection.")
        sys.exit(1)

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
    try:
        print("Setting up SerialInterface for listening...")
        local = create_serial_interface(serial_port)
        if not local:
            print("Failed to create SerialInterface for listening")
            sys.exit(1)
        print("SerialInterface setup for listening.")
    except Exception as e:
        print(f"Error setting up SerialInterface: {e}")
        print(f"Error type: {type(e).__name__}")
        print(f"Error details: {e.__dict__ if hasattr(e, '__dict__') else 'No details available'}")
        sys.exit(1)

    # Keep the script running to listen for messages
    try:
        while True:
            sys.stdout.flush()
            time.sleep(1)  # Sleep to reduce CPU usage
    except KeyboardInterrupt:
        print("Script terminated by user")
        if local:
            try:
                local.close()
            except:
                pass
    except Exception as e:
        print(f"Error during message listening: {e}")
        if local:
            try:
                local.close()
            except:
                pass

if __name__ == "__main__":
    main()
