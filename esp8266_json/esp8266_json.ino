#include <ArduinoJson.h>
#include "DHTesp.h"
#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>

#define LED 2  

#ifdef ESP32
#pragma message(THIS EXAMPLE IS FOR ESP8266 ONLY!)
#error Select ESP8266 board.
#endif
const String url = "http://e050-1-38-182-39.ngrok.io";
DHTesp dht;
const char* ssid = "Juhi";
const char* pass = "juhi1010";

void SetupPipeController(){
  Serial.begin(115200);
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  String thisBoard= ARDUINO_BOARD;
  Serial.println(thisBoard);
  dht.setup(16, DHTesp::DHT22);
  WiFi.begin(ssid, pass);
  while (WiFi.status() != WL_CONNECTED)
  {
    digitalWrite(LED,LOW); 
    delay(300);
    digitalWrite(LED,HIGH);
    delay(300);
    Serial.print(".");
  }
  Serial.println();
  Serial.println("WiFi Connected");
  digitalWrite(LED,LOW);
}


String createJsonString(){
    float temp = dht.getTemperature();
    DynamicJsonDocument root(200);
    root["temprature"] = temp;
    String s;
    serializeJson(root, s);  
    return s;
}



void setup() {
  SetupPipeController();
}



void loop() {
  if(Serial.read() == 'g'){
    HTTPClient http;
    WiFiClient wifi;
    String path = url +  "/Rajkot/Area1";
    http.begin(wifi, path);
    int statusCode = http.GET();

      if (statusCode>0) {
        Serial.print("HTTP Response code: ");
        Serial.println(statusCode);
        String payload = http.getString();
        Serial.println(payload);
      }
      else {
        Serial.print("Error code: ");
        Serial.println(statusCode);
      }
  }
}
