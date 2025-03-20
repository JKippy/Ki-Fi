import subprocess
import time
from datetime import datetime
import pandas as pd
import os
import json

# Track received message IDs to prevent duplicates
received_messages = set()

def process_message(message_data):
    """Process a received message and save it to Excel."""
    try:
        # Skip if we've already seen this message
        if message_data.get('id') in received_messages:
            return
            
        # Add message ID to received set
        received_messages.add(message_data.get('id'))
        
        print("\nReceived message:", message_data)
        message = {
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'text': message_data.get('decoded', {}).get('text', ''),
            'from': message_data.get('from', 'unknown'),
            'to': message_data.get('to', 'broadcast')
        }
        print(f"Processed message: {message}")
        save_to_excel([message])
    except Exception as e:
        print(f"Error processing message: {e}")

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

def check_device_connection():
    """Check if a Meshtastic device is connected."""
    try:
        result = subprocess.run(['meshtastic', '--info'], 
                              capture_output=True, 
                              text=True)
        return result.returncode == 0
    except Exception:
        return False

def main():
    print("Ki-Fi Receiver")
    print("Checking device connection...")
    
    if not check_device_connection():
        print("Error: No Meshtastic device found. Please connect a device and try again.")
        return
        
    print("Device connected successfully!")
    print("Starting message monitoring...")
    print("Press Ctrl+C to exit")
    
    try:
        while True:
            # Use meshtastic CLI to get messages
            result = subprocess.run(['meshtastic', '--get-messages'], 
                                 capture_output=True, 
                                 text=True)
            
            if result.returncode == 0:
                try:
                    messages = json.loads(result.stdout)
                    if messages:
                        for msg in messages:
                            process_message(msg)
                except json.JSONDecodeError:
                    pass  # No valid messages to process
            
            time.sleep(1)  # Check for new messages every second
            
    except KeyboardInterrupt:
        print("\nExiting...")

if __name__ == "__main__":
    main() 