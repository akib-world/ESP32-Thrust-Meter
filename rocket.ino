#include "BluetoothSerial.h"
#include <HX711_ADC.h>

#define DT 21
#define SCK 22

HX711_ADC LoadCell(DT, SCK);
BluetoothSerial SerialBT;

void setup() {

  Serial.begin(115200);      
  SerialBT.begin("ESP32_ThrustMeter"); 
  
  LoadCell.begin();
  LoadCell.start(2000);
  LoadCell.setCalFactor(1000.0); 
  
  Serial.println("ডুয়াল মোড থ্রাস্ট মিটার রেডি!");
  SerialBT.println("ডুয়াল মোড থ্রাস্ট মিটার রেডি!");
}

void loop() {
  LoadCell.update();
  float thrust = LoadCell.getData();
  unsigned long time = millis() / 1000;
  

  String data = "{\"time\":" + String(time) + ",\"thrust\":" + String(thrust) + "}";
  

  Serial.println(data);   
  SerialBT.println(data); 
  
  delay(100);
}
