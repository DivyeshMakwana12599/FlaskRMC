#include <ArduinoJson.h>
#include "DHTesp.h"
#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>

#define LED 2  

#ifdef ESP32
#pragma message(THIS EXAMPLE IS FOR ESP8266 ONLY!)
#error Select ESP8266 board.
#endif

DHTesp dht;

const String url = "http://792f-8-17-206-80.ngrok.io";
const char* ssid = "ASUS_ROG";
const char* pass = "16013010";


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


void getRequestPipe(String s){
  HTTPClient http;
  WiFiClient wifi;
  String path = url +  s;
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
    http.end();
}


String createJsonString(){
    float temp = dht.getTemperature();
    DynamicJsonDocument root(200);
    root["Temperature"] = temp;
    String s;
    serializeJson(root, s);  
    return s;
}




void setup() {
  SetupPipeController();
}




void loop() {
  if(Serial.read() == 'p'){
    WiFiClient wifi;
    HTTPClient http;
    http.addHeader("Content-Type", "application/json");
    String path = url + "/Umbergaon/NewGIDC/DivyeshHouse";
    http.begin(wifi, path);
    int statusCode = http.POST(createJsonString());
    Serial.print("HTTP Response code: ");
    Serial.println(statusCode);
    http.end();
  }
}
