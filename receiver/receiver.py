import meshtastic
import meshtastic.serial_interface
import time
from datetime import datetime
import pandas as pd
import os

def connect_to_device():
    """Connect to the Meshtastic device."""
    try:
        interface = meshtastic.serial_interface.SerialInterface()
        return interface
    except Exception as e:
        print(f"Error connecting to device: {e}")
        return None

def get_messages(interface):
    """Get messages from the device."""
    try:
        messages = interface.getMyNode().get("messages", [])
        return messages
    except Exception as e:
        print(f"Error getting messages: {e}")
        return []

def save_to_excel(messages, filename="received_messages.xlsx"):
    """Save messages to an Excel file."""
    try:
        # Convert messages to DataFrame
        df = pd.DataFrame(messages)
        
        # Add timestamp if not present
        if 'timestamp' not in df.columns:
            df['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Create Excel writer
        with pd.ExcelWriter(filename, engine='xlsxwriter') as writer:
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
            worksheet.set_column('A:A', 20)  # Timestamp column
            worksheet.set_column('B:B', 50)  # Message column
            
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
    print("Press Ctrl+C to exit and save messages")
    
    try:
        while True:
            messages = get_messages(interface)
            if messages:
                print(f"\nReceived {len(messages)} new messages")
                for msg in messages:
                    print(f"Message: {msg.get('text', '')}")
                save_to_excel(messages)
            time.sleep(1)  # Check for new messages every second
    except KeyboardInterrupt:
        print("\nExiting and saving messages...")
        messages = get_messages(interface)
        if messages:
            save_to_excel(messages)
    finally:
        interface.close()

if __name__ == "__main__":
    main() 