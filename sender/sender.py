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

def get_node_info():
    """Get information about the current node."""
    try:
        result = subprocess.run(['meshtastic', '--info'], 
                              capture_output=True, 
                              text=True)
        if result.returncode == 0:
            # Parse the output to get the node ID
            for line in result.stdout.split('\n'):
                if 'Node ID:' in line:
                    return line.split(':')[1].strip()
        return None
    except Exception:
        return None

def send_message(message, target_node_id):
    """Send a message via Meshtastic CLI to a specific node."""
    try:
        print(f"Attempting to send message to node {target_node_id}: {message}")
        # Use meshtastic CLI to send message to specific node
        result = subprocess.run(['meshtastic', '--sendtext', message, '--dest', str(target_node_id)], 
                              capture_output=True, 
                              text=True)
        
        if result.returncode == 0:
            print(f"Message sent successfully to node {target_node_id}: {message}")
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
    
    # Get the current node's ID
    current_node_id = get_node_info()
    if not current_node_id:
        print("Error: Could not get current node ID")
        return
    
    print(f"Current node ID: {current_node_id}")
    
    # Get the target node ID from user input
    while True:
        try:
            target_node_id = str(input("Enter the target node ID to send messages to: "))
            if target_node_id == current_node_id:
                print("Error: Cannot send messages to yourself")
                continue
            break
        except ValueError:
            print("Please enter a valid number for the node ID.")
    
    print(f"Enter messages to send to node {target_node_id} (press Ctrl+C to exit):")
    print("Note: Messages will only be sent to this specific node.")
    
    try:
        while True:
            message = input("> ")
            if message:
                send_message(message, target_node_id)
    except KeyboardInterrupt:
        print("\nExiting...")

if __name__ == "__main__":
    main() 