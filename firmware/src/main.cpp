#include <Arduino.h>
#include "sniffer_config.h"

struct SnifferStats {
  unsigned long frames = 0;
  unsigned long errors = 0;
  unsigned long filtered = 0;
};

SnifferStats stats;

struct CanFrame {
  unsigned long id;
  byte length;
  byte data[8];
  unsigned long timestampMs;
  bool extended;
};

bool setupMCP2515() {
  pinMode(MCP2515_CS_PIN, OUTPUT);
  pinMode(MCP2515_INT_PIN, INPUT_PULLUP);
  digitalWrite(MCP2515_CS_PIN, HIGH);
  Serial.print("MCP2515_INIT bitrate=");
  Serial.println(CAN_BITRATE);
  return true;
}

bool acceptFrame(const CanFrame& frame) {
  if (!frame.extended) {
    stats.filtered++;
    return false;
  }
  return true;
}

void printFrame(const CanFrame& frame) {
  Serial.print(frame.timestampMs);
  Serial.print(",0x");
  Serial.print(frame.id, HEX);
  Serial.print(",");
  Serial.print(frame.length);
  Serial.print(",");
  for (byte i = 0; i < frame.length; i++) {
    if (i > 0) {
      Serial.print(" ");
    }
    if (frame.data[i] < 16) {
      Serial.print("0");
    }
    Serial.print(frame.data[i], HEX);
  }
  Serial.println();
}

bool readSyntheticFrame(CanFrame& frame) {
  static byte counter = 0;
  frame.timestampMs = millis();
  frame.id = counter % 2 == 0 ? 0x18F00401 : 0x18EAFF33;
  frame.length = counter % 2 == 0 ? 8 : 3;
  frame.extended = true;
  for (byte i = 0; i < frame.length; i++) {
    frame.data[i] = counter + i;
  }
  counter++;
  delay(250);
  return true;
}

void setup() {
  Serial.begin(SERIAL_BAUDRATE);
  Serial.println("CAN_J1939_FIRMWARE_SNIFFER_LAB_BOOT");
  if (!setupMCP2515()) {
    stats.errors++;
    Serial.println("MCP2515_INIT_FAILED");
  }
}

void loop() {
  CanFrame frame{};
  if (!readSyntheticFrame(frame)) {
    stats.errors++;
    return;
  }
  if (!acceptFrame(frame)) {
    return;
  }
  stats.frames++;
  printFrame(frame);
}

