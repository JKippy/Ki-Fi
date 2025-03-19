# Ki-Fi LoRa Communication System

A solution for sending data from the competition area to the pits at FRC competitions without breaking E301 or using boat cellular.

Why this doesn't break rule E301: Using LoRa (Long Range Radio) does not violate E301 because LoRa operates on different communication frequencies and protocols that are distinct from the Wi-Fi standards mentioned (802.11a/b/g/n/ac/ax/be). E301 specifically targets the creation of Wi-Fi networks (i.e., access points or ad-hoc networks) using those specific protocols, as they can potentially interfere with the field network. LoRa, however, uses its own low-power, long-range communication protocol designed for low-bandwidth applications, and it doesn't fall under the 802.11 Wi-Fi standard, thus it's not considered a violation of the rule.

This project implements a LoRa communication system using two Heltec v3 devices:
1. A sender device that allows users to input messages and send them over LoRa
2. A receiver device that receives messages and logs them to an Excel file

## Hardware Requirements
- 2x Heltec v3 devices
- USB cables for programming
- Computer with Arduino IDE installed

## Software Requirements
- Arduino IDE
- Required libraries:
  - Heltec ESP32 Dev-Boards
  - LoRa
  - XLSXWriter (for Excel file handling)

## Project Structure
- `sender/` - Code for the sending Heltec v3 device
- `receiver/` - Code for the receiving Heltec v3 device
- `shared/` - Shared LoRa communication code
- `requirements.txt` - Python dependencies (for Excel handling)

## Setup Instructions
1. Install Arduino IDE
2. Install required libraries through Arduino Library Manager
3. Upload sender code to first Heltec v3
4. Upload receiver code to second Heltec v3
5. Connect both devices to power
6. Use the sender's interface to input and send messages
7. Check the Excel file on the receiver's SD card for received messages

## Configuration
- LoRa frequency: 915MHz (configurable)
- Spreading factor: 7
- Bandwidth: 125kHz
- Coding rate: 4/5
