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

// Button pins
const int UP_BTN = 35;
const int DOWN_BTN = 34;
const int SELECT_BTN = 39;

// Message buffer
char messageBuffer[240];
int currentPosition = 0;
bool isEditing = true;

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
  
  // Setup button pins
  pinMode(UP_BTN, INPUT);
  pinMode(DOWN_BTN, INPUT);
  pinMode(SELECT_BTN, INPUT);
  
  // Initial display
  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(SSD1306_WHITE);
  display.setCursor(0,0);
  display.println("Ki-Fi Sender");
  display.println("Enter message:");
  display.display();
}

void loop() {
  if (isEditing) {
    handleMessageEditing();
  } else {
    handleMessageSending();
  }
}

void handleMessageEditing() {
  if (digitalRead(UP_BTN) == LOW) {
    if (currentPosition < 239) {
      messageBuffer[currentPosition++] = 'A';
      updateDisplay();
    }
  }
  
  if (digitalRead(DOWN_BTN) == LOW) {
    if (currentPosition < 239) {
      messageBuffer[currentPosition++] = 'B';
      updateDisplay();
    }
  }
  
  if (digitalRead(SELECT_BTN) == LOW) {
    if (currentPosition > 0) {
      messageBuffer[--currentPosition] = '\0';
      updateDisplay();
    } else {
      isEditing = false;
      display.clearDisplay();
      display.setCursor(0,0);
      display.println("Message ready to send:");
      display.println(messageBuffer);
      display.println("\nPress SELECT to send");
      display.display();
    }
  }
}

void handleMessageSending() {
  if (digitalRead(SELECT_BTN) == LOW) {
    // Send message
    LoRa.beginPacket();
    LoRa.print(messageBuffer);
    LoRa.endPacket();
    
    // Reset for next message
    currentPosition = 0;
    memset(messageBuffer, 0, sizeof(messageBuffer));
    isEditing = true;
    
    display.clearDisplay();
    display.setCursor(0,0);
    display.println("Message sent!");
    display.println("Enter new message:");
    display.display();
  }
}

void updateDisplay() {
  display.clearDisplay();
  display.setCursor(0,0);
  display.println("Ki-Fi Sender");
  display.println("Enter message:");
  display.println(messageBuffer);
  display.println("\nUse UP/DOWN to type");
  display.println("SELECT to delete/send");
  display.display();
} 