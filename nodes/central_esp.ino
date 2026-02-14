#include <SPI.h>
#include <LoRa.h>

#define SS 5
#define RST 14
#define DIO0 26
#define LORA_FREQ 433E6

void setup() {
  Serial.begin(115200);
  LoRa.setPins(SS, RST, DIO0);

  if (!LoRa.begin(LORA_FREQ)) {
    while (1);
  }

  LoRa.setSpreadingFactor(7);
  LoRa.setSignalBandwidth(250E3);
  LoRa.setCodingRate4(5);
  LoRa.enableCrc();
  LoRa.setTxPower(20);

  Serial.println("LoRa TEXT MODE READY");
}

void loop() {

  // -------- SERIAL → LORA --------
  if (Serial.available()) {

    String msg = Serial.readStringUntil('\n');
    msg.trim();  // remove \r \n spaces

    if (msg.length() > 0) {
      LoRa.beginPacket();
      LoRa.print(msg);   // send EXACTLY as python sent
      LoRa.endPacket();
    }
  }

  // -------- LORA → SERIAL --------
  int packetSize = LoRa.parsePacket();

  if (packetSize) {

    String received = "";

    while (LoRa.available()) {
      received += (char)LoRa.read();
    }

    received.trim();

    // 🔥 IMPORTANT: print RAW packet only
    Serial.println(received);
  }
}
