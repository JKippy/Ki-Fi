import meshtastic
import meshtastic.serial_interface
import time
from datetime import datetime
import pandas as pd
import os

# Track received message IDs to prevent duplicates
received_messages = set()

def on_message(packet, interface):
    """Callback function for received messages."""
    try:
        # Skip if we've already seen this message
        if packet.get('id') in received_messages:
            return
            
        # Add message ID to received set
        received_messages.add(packet.get('id'))
        
        print("\nReceived packet:", packet)  # Debug: Print raw packet
        message = {
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'text': packet.get('decoded', {}).get('text', ''),
            'from': packet.get('from', 'unknown'),
            'to': packet.get('to', 'broadcast')
        }
        print(f"Processed message: {message}")  # Debug: Print processed message
        save_to_excel([message])
    except Exception as e:
        print(f"Error processing message: {e}")
        print(f"Packet contents: {packet}")  # Debug: Print packet on error

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
        
        # Set up message callback
        interface.onReceive = on_message
        return interface
    except Exception as e:
        print(f"Error connecting to device: {e}")
        return None

def save_to_excel(messages, filename="received_messages.xlsx"):
    """Save messages to an Excel file."""
    try:
        # Convert messages to DataFrame
        df = pd.DataFrame(messages)
        
        # Create Excel writer
        with pd.ExcelWriter(filename, engine='xlsxwriter') as writer:
            # If file exists, load existing data and append new messages
            if os.path.exists(filename):
                existing_df = pd.read_excel(filename)
                df = pd.concat([existing_df, df], ignore_index=True)
            
            df.to_excel(writer, sheet_name='Messages', index=False)
            
            # Get the workbook and worksheet objects
            workbook = writer.book
            worksheet = writer.sheets['Messages']
            
            # Define formats
            header_format = workbook.add_format({
                'bold': True,
                'bg_color': '#4B0082',
                'font_color': 'white',
                'border': 1
            })
            
            cell_format = workbook.add_format({
                'border': 1,
                'text_wrap': True
            })
            
            # Format the header
            for col_num, value in enumerate(df.columns.values):
                worksheet.write(0, col_num, value, header_format)
            
            # Set column widths
            for col_num, column in enumerate(df.columns):
                max_length = max(df[column].astype(str).apply(len).max(), len(column))
                worksheet.set_column(col_num, col_num, max_length + 2)
            
            # Format all cells
            for row in range(1, len(df) + 1):
                for col in range(len(df.columns)):
                    worksheet.write(row, col, df.iloc[row-1, col], cell_format)
        
        print(f"Messages saved to {filename}")
    except Exception as e:
        print(f"Error saving to Excel: {e}")

def main():
    print("Ki-Fi Receiver")
    print("Connecting to device...")
    
    interface = connect_to_device()
    if not interface:
        print("Failed to connect to device. Exiting...")
        return
    
    print("Connected successfully!")
    print("Waiting for messages...")
    print("Press Ctrl+C to exit")
    
    try:
        while True:
            time.sleep(1)  # Keep the script running
    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        interface.close()

if __name__ == "__main__":
    main() 