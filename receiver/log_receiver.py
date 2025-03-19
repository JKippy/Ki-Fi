import serial
import time
from datetime import datetime

def main():
    # Configure serial port (adjust port as needed)
    ser = serial.Serial(
        port='/dev/ttyUSB0',  # Change this to match your system
        baudrate=115200,
        timeout=1
    )
    
    # Open log file
    log_file = open('received_messages.txt', 'a')
    
    print("Ki-Fi Receiver Logger")
    print("Waiting for messages...")
    
    try:
        while True:
            if ser.in_waiting:
                line = ser.readline().decode('utf-8').strip()
                if line:
                    # Add timestamp to log
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    log_file.write(f"[{timestamp}] {line}\n")
                    log_file.flush()  # Ensure immediate write
                    print(line)  # Also print to console
    except KeyboardInterrupt:
        print("\nLogging stopped")
    finally:
        ser.close()
        log_file.close()

if __name__ == "__main__":
    main() 