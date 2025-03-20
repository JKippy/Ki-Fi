import subprocess
import time
from datetime import datetime
from cryptography.fernet import Fernet
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

def generate_key(password):
    """Generate a key from a password using PBKDF2"""
    salt = b'kifi_salt'  # In production, use a random salt and store it securely
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return key

def encrypt_message(message, key):
    """Encrypt a message using Fernet (AES-128-CBC)"""
    f = Fernet(key)
    encrypted_message = f.encrypt(message.encode())
    return encrypted_message.decode()

def check_device_connection():
    """Check if a Meshtastic device is connected."""
    try:
        result = subprocess.run(['meshtastic', '--info'], 
                              capture_output=True, 
                              text=True)
        return result.returncode == 0
    except Exception:
        return False

def send_message(message, target_node_id, encryption_key):
    """Send an encrypted message via Meshtastic CLI to a specific node."""
    try:
        # Encrypt the message
        encrypted_message = encrypt_message(message, encryption_key)
        print(f"Attempting to send encrypted message to node {target_node_id}")
        
        # Use meshtastic CLI to send message to specific node
        result = subprocess.run(['meshtastic', '--sendtext', encrypted_message, '--dest', str(target_node_id)], 
                              capture_output=True, 
                              text=True)
        
        if result.returncode == 0:
            print(f"Encrypted message sent successfully to node {target_node_id}")
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
        print("Error: No Meshtastic device is found. Please connect a device and try again.")
        return
        
    print("Device connected successfully!")
    
    # Get the target node ID from user input
    while True:
        try:
            target_node_id = int(input("Enter the target node ID to send messages to: "))
            break
        except ValueError:
            print("Please enter a valid number for the node ID.")
    
    # Get encryption password from user
    password = input("Enter the encryption password: ")
    encryption_key = generate_key(password)
    
    print(f"Enter messages to send to node {target_node_id} (press Ctrl+C to exit):")
    print("Messages will be encrypted before sending.")
    
    try:
        while True:
            message = input("> ")
            if message:
                send_message(message, target_node_id, encryption_key)
    except KeyboardInterrupt:
        print("\nExiting...")

if __name__ == "__main__":
    main() 