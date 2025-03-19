import meshtastic
import meshtastic.serial_interface
import time
from datetime import datetime

def connect_to_device():
    """Connect to the Meshtastic device."""
    try:
        interface = meshtastic.serial_interface.SerialInterface()
        
        # Configure for secure communication
        node = interface.getLocalNode()
        # Set a custom channel name (this acts as a password)
        node.setConfig('lora.channel_name', 'KiFiSecure')
        # Set a custom PSK (Pre-Shared Key)
        node.setConfig('lora.psk', 'KiFiSecretKey123')
        # Set the modem preset for better range
        node.setConfig('lora.modem_preset', 'LONG_FAST')
        
        return interface
    except Exception as e:
        print(f"Error connecting to device: {e}")
        return None

def send_message(interface, message):
    """Send a message via Meshtastic."""
    try:
        print(f"Attempting to send message: {message}")  # Debug: Print attempt
        # Send the message
        interface.sendText(message)
        print(f"Message sent successfully: {message}")
        print("Waiting for acknowledgment...")  # Debug: Print waiting status
        return True
    except Exception as e:
        print(f"Error sending message: {e}")
        print(f"Error type: {type(e)}")  # Debug: Print error type
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