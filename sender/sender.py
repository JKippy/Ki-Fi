import meshtastic
import meshtastic.serial_interface
import time
from datetime import datetime

def connect_to_device():
    """Connect to the Meshtastic device."""
    try:
        interface = meshtastic.serial_interface.SerialInterface()
        return interface
    except Exception as e:
        print(f"Error connecting to device: {e}")
        return None

def send_message(interface, message):
    """Send a message via Meshtastic."""
    try:
        # Configure for broadcast mode
        interface.getMyNode().setConfig('lora.modem_preset', 'LONG_FAST')
        interface.getMyNode().setConfig('lora.tx_power', 20)
        
        # Send the message
        interface.sendText(message, wantAck=True)
        print(f"Message sent successfully: {message}")
        return True
    except Exception as e:
        print(f"Error sending message: {e}")
        return False

def main():
    print("Ki-Fi Sender")
    print("Connecting to device...")
    
    interface = connect_to_device()
    if not interface:
        print("Failed to connect to device. Exiting...")
        return
    
    print("Connected successfully!")
    print("Enter messages to send (press Ctrl+C to exit):")
    
    try:
        while True:
            message = input("> ")
            if message:
                send_message(interface, message)
    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        interface.close()

if __name__ == "__main__":
    main() 