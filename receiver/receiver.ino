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
int messageCount = 0;

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
  display.println("Ki-Fi Receiver");
  display.println("Waiting for messages...");
  display.display();
  
  // Print status to Serial
  Serial.println("Ki-Fi Receiver");
  Serial.println("Waiting for messages...");
}

void loop() {
  // Check for incoming packets
  int packetSize = LoRa.parsePacket();
  if (packetSize) {
    // Read the packet
    int i = 0;
    while (LoRa.available() && i < 239) {
      messageBuffer[i++] = (char)LoRa.read();
    }
    messageBuffer[i] = '\0';
    
    // Get timestamp
    unsigned long timestamp = millis();
    
    // Print to Serial
    Serial.print("Message #");
    Serial.print(++messageCount);
    Serial.print(" [");
    Serial.print(timestamp);
    Serial.println("ms]:");
    Serial.println(messageBuffer);
    
    // Update display
    display.clearDisplay();
    display.setCursor(0,0);
    display.println("Ki-Fi Receiver");
    display.println("Message received:");
    display.println(messageBuffer);
    display.println("\nMessages:");
    display.println(messageCount);
    display.display();
  }
} 