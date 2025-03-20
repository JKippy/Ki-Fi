import subprocess
import time
from datetime import datetime

def check_device_connection():
    """Check if a Meshtastic device is connected."""
    try:
        result = subprocess.run(['meshtastic', '--info'], 
                              capture_output=True, 
                              text=True)
        return result.returncode == 0
    except Exception:
        return False

def send_message(message):
    """Send a message via Meshtastic CLI."""
    try:
        print(f"Attempting to send message: {message}")
        # Use meshtastic CLI to send message
        result = subprocess.run(['meshtastic', '--sendtext', message], 
                              capture_output=True, 
                              text=True)
        
        if result.returncode == 0:
            print(f"Message sent successfully: {message}")
            return True
        else:
            print(f"Error sending message: {result.stderr}")
            return False
    except Exception as e:
        print(f"Error sending message: {e}")
        return False

def main():
    print("Ki-Fi Sender")
    print("Checking device connection...")
    
    if not check_device_connection():
        print("Error: No Meshtastic device found. Please connect a device and try again.")
        return
        
    print("Device connected successfully!")
    print("Enter messages to send (press Ctrl+C to exit):")
    
    try:
        while True:
            message = input("> ")
            if message:
                send_message(message)
    except KeyboardInterrupt:
        print("\nExiting...")

if __name__ == "__main__":
    main() 