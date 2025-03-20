# Ki-Fi: Private Mesh Network Communication

A solution for sending data from the competition area to the pits at FRC competitions without breaking E301 or using boat cellular.
Why this doesn't break rule E301: Using LoRa (Long Range Radio) does not violate E301 because LoRa operates on different communication 
frequencies and protocols that are distinct from the Wi-Fi standards mentioned (802.11a/b/g/n/ac/ax/be). E301 specifically targets the 
creation of Wi-Fi networks (i.e., access points or ad-hoc networks) using those specific protocols, as they can potentially interfere with 
the field network. LoRa, however, uses its own low-power, long-range communication protocol designed for low-bandwidth applications, and it 
doesn't fall under the 802.11 Wi-Fi standard, thus it's not considered a violation of the rule.

Ki-Fi is a secure, private communication system built on the Meshtastic mesh network platform. It enables direct, private messaging between two specific nodes, ensuring that messages can only be sent and received by authorized devices.

## Features

- **Private Messaging**: Messages can only be sent between two specific nodes
- **Node Validation**: Prevents sending messages to yourself
- **Message Logging**: All received messages are logged with timestamps
- **Device Connection Validation**: Automatic detection and validation of Meshtastic devices
- **Cross-Platform Support**: Works on macOS, Linux, and Windows

## Prerequisites

- Python 3.7 or higher
- Meshtastic device (connected via USB)
- Meshtastic CLI tools installed
- Required Python packages:
  ```bash
  pip install meshtastic
  pip install pyserial
  pip install pubsub
  ```

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/Ki-Fi.git
   cd Ki-Fi
   ```

2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Connect your Meshtastic device via USB

## Usage

### Setting Up the Receiver

1. Run the receiver:
   ```bash
   python receiver/receiver.py
   ```

2. The receiver will:
   - Display the current node ID
   - Show a list of available nodes
   - Prompt you to enter the sender's node ID
   - Only accept messages from the specified sender

### Setting Up the Sender

1. Run the sender:
   ```bash
   python sender/sender.py
   ```

2. The sender will:
   - Display the current node ID
   - Prompt you to enter the receiver's node ID
   - Only send messages to the specified receiver

### Sending Messages

1. In the sender terminal:
   - Type your message and press Enter
   - Messages will only be sent to the specified receiver
   - Press Ctrl+C to exit

### Receiving Messages

1. In the receiver terminal:
   - Messages from the specified sender will be displayed
   - Messages from other nodes will be ignored
   - All received messages are logged to `meshtastic_messages.txt`
   - Press Ctrl+C to exit

## Message Logging

All received messages are automatically logged to `meshtastic_messages.txt` in the following format:
```
[YYYY-MM-DD HH:MM:SS] SenderName: Message
```

## Security Features

- Messages can only be sent between two specific nodes
- The receiver ignores messages from unauthorized nodes
- The sender can only send to one specific receiver
- Node validation prevents self-messaging

## Troubleshooting

1. **Device Not Found**
   - Ensure your Meshtastic device is properly connected via USB
   - Check USB permissions
   - Try unplugging and replugging the device

2. **Message Not Received**
   - Verify both nodes are using the correct node IDs
   - Check that the sender and receiver are properly configured
   - Ensure both devices are within range

3. **Connection Issues**
   - Check USB connection
   - Verify Meshtastic CLI tools are installed
   - Try restarting the application

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
