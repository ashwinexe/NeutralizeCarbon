#include <ESP8266WiFi.h>
#include <WiFiClientSecure.h> 
#include <ESP8266WebServer.h>
#include <ESP8266HTTPClient.h>
#include<dht11.h>

dht11 DHT;
const char* ssid = "Trikuldham";
const char* password = "jaihanuman1981";
const char *host = "neutralizecarbon.neeltron.repl.co";
const int httpsPort = 443;
const char fingerprint[] PROGMEM = "9A F2 61 9E 52 05 CA 9A 6B B8 F0 DB 54 07 18 39 E2 39 5D 36";

void setup(){
  Serial.begin(9600);
  WiFi.mode(WIFI_OFF);
  delay(1000);
  WiFi.mode(WIFI_STA);
  
  WiFi.begin(ssid, password);
  Serial.println("");

  Serial.print("Connecting");
  // Wait for connection
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.print("Connected to ");
  Serial.println(ssid);
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
}

void loop(){
  int chk = DHT.read(2);
  Serial.print("Temperature = ");
  Serial.println(DHT.temperature);
  Serial.print("Humidity = ");
  Serial.println(DHT.humidity);

  WiFiClientSecure httpsClient;
  Serial.println(host);
  Serial.printf("Using fingerprint '%s'\n", fingerprint);
  httpsClient.setFingerprint(fingerprint);
  httpsClient.setTimeout(15000); // 15 Seconds
  delay(1000);
  
  Serial.print("HTTPS Connecting");
  int r=0; //retry counter
  while((!httpsClient.connect(host, httpsPort)) && (r < 30)){
      delay(100);
      Serial.print(".");
      r++;
  }
  if(r==30) {
    Serial.println("Connection failed");
  }
  else {
    Serial.println("Connected to web");
  }
  
  String getData, Link;

  Link = "/input?temperature="+String(DHT.temperature)+"&humidity="+String(DHT.humidity)+"&location=Jaipur&N=24.6&P=11.3&K=1&rainfall=100&ph=7&vh=3&ah=500&rh=2";
  Serial.print("requesting URL: ");
  Serial.println(host+Link);
  httpsClient.print(String("GET ") + Link + " HTTP/1.1\r\n" +
               "Host: " + host + "\r\n" +               
               "Connection: close\r\n\r\n");

  Serial.println("request sent");
                  
  while (httpsClient.connected()) {
    String line = httpsClient.readStringUntil('\n');
    if (line == "\r") {
      Serial.println("received");
      break;
    }
  }

  String line;
  while(httpsClient.available()){        
    line = httpsClient.readStringUntil('\n');
    Serial.println(line);
  }
  delay(10000);
}
