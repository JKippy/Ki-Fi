#include <SPI.h>
#include <LoRa.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

// OLED display settings
#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define OLED_RESET -1
#define SCREEN_ADDRESS 0x3C

// LoRa settings
#define SS 8
#define RST 12
#define DIO0 14
#define BAND 915E6

// Initialize display
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

// Message buffer
char messageBuffer[240];
bool isWaitingForInput = true;

void setup() {
  Serial.begin(115200);
  
  // Initialize OLED
  if(!display.begin(SSD1306_SWITCHCAPVCC, SCREEN_ADDRESS)) {
    Serial.println(F("SSD1306 allocation failed"));
    for(;;);
  }
  
  // Initialize LoRa
  LoRa.setPins(SS, RST, DIO0);
  if (!LoRa.begin(BAND)) {
    Serial.println("LoRa initialization failed!");
    while (1);
  }
  
  // Configure LoRa parameters
  LoRa.setSpreadingFactor(7);
  LoRa.setSignalBandwidth(125E3);
  LoRa.setCodingRate4(5);
  
  // Initial display
  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(SSD1306_WHITE);
  display.setCursor(0,0);
  display.println("Ki-Fi Sender");
  display.println("Ready to send");
  display.display();
  
  // Print instructions to Serial
  Serial.println("Ki-Fi Sender");
  Serial.println("Enter message to send (max 240 chars):");
}

void loop() {
  if (Serial.available()) {
    String input = Serial.readStringUntil('\n');
    input.trim(); // Remove whitespace
    
    if (input.length() > 0) {
      // Limit message length
      if (input.length() > 240) {
        input = input.substring(0, 240);
      }
      
      // Send message
      LoRa.beginPacket();
      LoRa.print(input);
      LoRa.endPacket();
      
      // Update display
      display.clearDisplay();
      display.setCursor(0,0);
      display.println("Ki-Fi Sender");
      display.println("Message sent:");
      display.println(input);
      display.display();
      
      // Print confirmation
      Serial.println("Message sent successfully!");
      Serial.println("Enter next message:");
    }
  }
} 