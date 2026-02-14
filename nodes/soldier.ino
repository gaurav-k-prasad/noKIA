#include <SPI.h>
#include <LoRa.h>
#include <TinyGPS++.h>
#include <Wire.h>
#include <QMC5883LCompass.h>

#define SS 5
#define RST 14
#define DIO0 26
#define LORA_FREQ 433E6

#define GPS_RX 16
#define GPS_TX 17

float offsetX = -346;
float offsetY = 1189;
float scaleX = 1.18;
float declinationAngle = 2.0;

HardwareSerial gpsSerial(2);
TinyGPSPlus gps;
QMC5883LCompass compass;

void setup()
{
  Serial.begin(115200);
  delay(1000);

  gpsSerial.begin(115200, SERIAL_8N1, GPS_RX, GPS_TX);

  Wire.begin(21, 22);
  compass.init();

  LoRa.setPins(SS, RST, DIO0);

  if (!LoRa.begin(LORA_FREQ))
  {
    while (1)
      ;
  }

  LoRa.setSpreadingFactor(7);
  LoRa.setSignalBandwidth(250E3);
  LoRa.setCodingRate4(5);
  LoRa.enableCrc();
  LoRa.setTxPower(14);

  Serial.println("NODE READY (CLEAN FORMAT)");
}

void loop()
{

  while (gpsSerial.available())
  {
    gps.encode(gpsSerial.read());
  }

  compass.read();

  float x = (compass.getX() - offsetX) * scaleX;
  float y = (compass.getY() - offsetY);

  float heading = atan2(y, x);
  heading = heading * 180 / PI;
  heading += declinationAngle;

  if (heading < 0)
    heading += 360;
  if (heading > 360)
    heading -= 360;

  // -------- SERIAL → LORA --------
  if (Serial.available())
  {
    String packet = "[S]";

    if (gps.location.isValid())
    {
      packet += String(gps.location.lat(), 6);
      packet += ",";
      packet += String(gps.location.lng(), 6);
    }
    else
    {
      packet += "0,0";
    }

    packet += "|";
    packet += String((int)heading);

    LoRa.beginPacket();
    LoRa.print(packet);
    LoRa.endPacket();

    Serial.println(packet);
  }

  int packetSize = LoRa.parsePacket();

  if (packetSize)
  {
    String received = "";
    while (LoRa.available())
    {
      received += (char)LoRa.read();
    }
    received.trim();
    Serial.println(received);
  }
}
