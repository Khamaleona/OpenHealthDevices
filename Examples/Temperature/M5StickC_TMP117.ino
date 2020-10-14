#include <Wire.h>
#include <SparkFun_TMP117.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <DNSServer.h>
#include <WebServer.h>
#include <M5StickC.h>
#include <EEPROM.h>
#include "FS.h"

/*
Temperature sensor development using M5StickC board. Through captive portal, we set wifi credentials in order to connect and send data to a remote server.
*/

#define uS_TO_S_FACTOR 1000000ULL  /* Conversion factor for micro seconds to seconds */
#define TIME_TO_SLEEP  55        /* Time ESP32 will go to sleep (in seconds) */
#define ssidDefault "ESP32WiFi"  // Enter SSID here
#define passwordDefault  "ICSTFM2020"  //Enter Password here

TMP117 temp;

bool wifiStatus = false;
bool portalStarted = false;

// To get date and time information
const char* ntpServer = "pool.ntp.org";
const long  gmtOffset_sec = 3600;
const int   daylightOffset_sec = 3600;
char timeStringBuff[50];

const byte DNS_PORT = 53;
IPAddress apIP(8, 8, 8, 8);
IPAddress netMsk(255, 255, 255, 0);
DNSServer dnsServer;
WebServer webServer(80);

bool conexion;
unsigned int status = WL_IDLE_STATUS;
const char * softAP_ssid = ssidDefault;
const char * softAP_password = passwordDefault;
const char * myHostname = "icstfm2020";
char ssid[33] = "";
char password[65] = "";
char serverName[40] = "";

void wifiClear(){
    WiFi.mode(WIFI_STA);
    WiFi.disconnect();
    wifiStatus = WiFi.status() == WL_CONNECTED;
    delay(100);
}

void wifiConnect(unsigned short tries){
  wifiStatus = WiFi.status() == WL_CONNECTED;
  Serial.print("Connecting");
  while((tries > 0) && (!wifiStatus)){
    wifiClear();
    WiFi.begin(ssid, password);
    delay(5000);
    wifiStatus = WiFi.status() == WL_CONNECTED;
    tries--;
    Serial.print(".");
  }
}

void wifiDisconnect(){
  WiFi.disconnect();
  WiFi.mode(WIFI_OFF);
  wifiStatus = false;
}

void printLocalTime(){
  struct tm timeinfo;
  if(!getLocalTime(&timeinfo)){
    Serial.println("Failed to obtain time");
    return;
  }
  strftime(timeStringBuff, sizeof(timeStringBuff), "%Y-%m-%d %H:%M:%S", &timeinfo);
}

void sendData(float tempC, char fecha[]){
  HTTPClient http;
  http.begin(serverName);
  http.addHeader("Content-Type", "application/json");

  //Building json
  String cadena = "{\"sensor\": \"0\",";
  cadena += "\"value\": \"";
  cadena += String(tempC); 
  cadena += "\",";
  cadena += "\"date\": \"";
  cadena += fecha;
  cadena += "\"}";

  Serial.print("JSON: ");
  Serial.println(cadena);

  int response = http.POST(cadena);

  if (response > 0) {
    Serial.print("HTTP Response Code: ");
    Serial.println(response);
    Serial.println(http.getString());
  } else {
    Serial.print("Error Code: ");
    Serial.println(response);
  }
  http.end();
}

bool isIP (String str){
  for(size_t i=0; i<str.length(); i++){
    char c = str.charAt(i);
    if (c != '.' && (c < '0' || c > '9')){
      return false;
    }
  }
  return true;
}

String toStringIP(IPAddress ip) {
  String res = "";
  for (int i = 0; i < 3; i++) {
    res += String((ip >> (8 * i)) & 0xFF) + ".";
  }
  res += String(((ip >> 8 * 3)) & 0xFF);
  return res;
}

bool captivePortal(){
  if(!isIP(webServer.hostHeader()) && webServer.hostHeader() != (String(myHostname) + ".local")){
    Serial.println("Request redirected to captive portal");
    webServer.sendHeader("Location", String("http://") + toStringIP(webServer.client().localIP()), true);
    webServer.send(302, "text/plain","");
    webServer.client().stop();
    return true;
  }
  return false;
}

void handleRoot(){
  Serial.println("HANDLE ROOT....");
  if(captivePortal()){
    return;
  }
  webServer.sendHeader("Cache-Control", "no-cache, no-store, must-revalidate");
  webServer.sendHeader("Pragma", "no-cache");
  webServer.sendHeader("Expires", "-1");

  String Page;
  Page += String(F("<!DOCTYPE html><html lang='es'><head>")) + 
            F("<meta name='viweport' content='width=device-width'>") +
            F("<title>CaptivePortal</title></head><body><h1>HELLO WORLD!!</h1>");
  if(webServer.client().localIP() == apIP){
    Page += String(F("<p>You are connected through the soft AP: ")) + softAP_ssid + F("</p>");
  }else{
    Page += String(F("<p>You are connected through the wifi network: ")) + ssid + F("</p>");
  }
  Page += F("<p> You may want to <a href='/wifi'>Config the wifi connection</a></p>");
  Page += F("<p> If you ended configuring ESP32, please click <a href='/finish'>HERE</a></p></body></html>");
  
  webServer.send(200, "text/html", Page);
}

void handleWifi(){
  webServer.sendHeader("Cache-Control", "no-cache, no-store, must-revalidate");
  webServer.sendHeader("Pragma", "no-cache");
  webServer.sendHeader("Expires", "-1");

  String Page;
  Page += String(F("<!DOCTYPE html><html lang='es'><head>")) + 
            F("<meta name='viewport' content='width=device-width'>") +
            F("<title>CaptivePortal</title></head><body><h1>Wifi Config</h1>");
  if(webServer.client().localIP() == apIP){
    Page += String(F("<p>You are connected through the soft AP: ")) + softAP_ssid + F("</p>");
  }else{
    Page += String(F("<p>You are connected through the wifi network: ")) + ssid + F("</p>");
  }
  Page += String(F("\r\n<br /><table><tr><th align='left'>SoftAP config</th></tr>""<tr><td>SSID ")) 
                  + String(softAP_ssid) + F("</td></tr><tr><td>IP ") + toStringIP(WiFi.softAPIP()) 
                  + F("</td></tr></table> \r\n<br /><table><tr><th align='left'>WLAN config</th></tr><tr><td>SSID ") 
                  + String(ssid) + F("</td></tr><tr><td>IP ") + 
                  toStringIP(WiFi.localIP()) + F("</td></tr></table> \r\n<br /><table><tr><th align='left'>WLAN list (refresh of any missing)</th></tr>");

  Serial.println("Scan start");
  int n = WiFi.scanNetworks();
  Serial.println("Scan done");
  if(n > 0){
    for(int i=0; i< n; i++){
      Page += String(F("\r\n<tr><td>SSID ")) + WiFi.SSID(i) + F(")</td></tr>");
    }
  }else{
    Page += F("<tr><td>No WLAN found</td></tr>");
  }
  Page += String(F("</table>")) +
          F("\r\n<br/> <form method='POST' action='/wifisave'><h4>Connect to network:</h4>")+
          F("<input type='text' placeholder='network' name='n'/>") +
          F("<br/> <input type='password' placeholder='password' name='p'/>") +
          F("<br/> <input type='text' placeholder='server' name='s'/>") +
          F("<br/> <input type='submit' value='Connect/Disconnect'/></form>") +
          F("<p>You may want to <a href='/'>Return to the home page</a></p></body></html>");
          
  webServer.send(200, "text/html", Page);
  webServer.client().stop(); //Stop is needed because we sent no content length        
}

void handleWifiSave(){
  Serial.println("WiFi Saving...");
  webServer.arg("n").toCharArray(ssid, sizeof(ssid) - 1);
  webServer.arg("p").toCharArray(password, sizeof(password) - 1);
  webServer.arg("s").toCharArray(serverName, sizeof(serverName)-1);
  webServer.sendHeader("Location", "wifi", true);
  webServer.sendHeader("Cache-Control", "no-cache, no-store, must-revalidate");
  webServer.sendHeader("Pragma", "no-cache");
  webServer.sendHeader("Expires", "-1");
  webServer.send(302, "text/plain", "");
  webServer.client().stop();
  saveCredentials();
  conexion = strlen(ssid) > 0;
}

void finishConfiguration(){
  webServer.close(); 
  portalStarted = false;
  ESP.restart();
}

void handleNotFound(){
  if(captivePortal()){
    return;
  }
  String message = F("File Not Found\n\n");
  message += F("URI: ");
  message += webServer.uri();
  message += F("\nMethod: ");
  message += (webServer.method() == HTTP_GET) ? "GET" : "POST";
  message += F("\nArguments: ");
  message += webServer.args();
  message += F("\n");

  for(uint8_t i=0; i< webServer.args(); i++){
    message += String(F(" ")) + webServer.argName(i) + F(": ") + webServer.arg(i) + F("\n");
  }

  webServer.sendHeader("Cache-Control", "no-cache, no-store, must-revalidate");
  webServer.sendHeader("Pragma", "no-cache");
  webServer.sendHeader("Expires", "-1");
  webServer.send(404, "text/plain", message);
}

void startCaptivePortal(){
  //Captive Portal Configuration
  M5.Lcd.fillScreen(BLACK);//Clear screen for the new message
  M5.Lcd.setCursor(0, 6, 2);
  M5.Lcd.setTextColor(WHITE, BLACK);
  M5.Lcd.setTextSize(1);
  M5.Lcd.printf("Starting Configuration Portal...");
  
  WiFi.mode(WIFI_AP);
  WiFi.persistent(false);
  WiFi.softAP(softAP_ssid, softAP_password);
  delay(2000); // VERY IMPORTANT
  WiFi.softAPConfig(apIP, apIP, IPAddress(255, 255, 255, 0));
  Serial.print("Web Server IP: ");
  Serial.println(apIP);
  Serial.print("SSID: ");
  Serial.println(softAP_ssid);
  Serial.print("Password: ");
  Serial.println(softAP_password);

  dnsServer.start(DNS_PORT, "*", apIP);

  webServer.on("/", handleRoot);
  webServer.on("/wifi", handleWifi);
  webServer.on("/wifisave", handleWifiSave);
  webServer.on("/finish", finishConfiguration);
  webServer.onNotFound(handleNotFound);
  
  webServer.begin();
  Serial.println("HTTP Server Started!");
  conexion = strlen(ssid) > 0; //Request WLAN connect if there is a SSID
}

void startSensor(){
  Serial.println("Starting TMP117...");
  if(temp.begin()){
    Serial.println("TMP117 OK");
  }else{
    Serial.println("TMP117 ERROR");
    M5.Lcd.fillScreen(BLACK);//Clear screen for the new message
    M5.Lcd.setCursor(0, 6, 2);
    M5.Lcd.setTextColor(WHITE, BLACK);
    M5.Lcd.setTextSize(1);
    M5.Lcd.printf("SENSOR IS NOT WORKING! RESTARTING...");
    delay(5000);
    ESP.restart();
  }

  float tempC;
  configTime(gmtOffset_sec, daylightOffset_sec, ntpServer);
  printLocalTime();
  
  if(temp.dataReady()){
    tempC = temp.readTempC();
    M5.Lcd.fillScreen(BLACK);//Clear screen for the new message
    M5.Lcd.setCursor(0, 6, 2);
    M5.Lcd.setTextColor(WHITE, BLACK);
    M5.Lcd.setTextSize(2);
    M5.Lcd.printf("Temp: %2.2fC", tempC);
    delay(5000); //Waiting 5 seconds to show the measure

    if(wifiStatus){
      sendData(tempC, timeStringBuff);
    }else{
      Serial.println("Wifi is disconnected");
      M5.Lcd.fillScreen(BLACK);//Clear screen for the new message
      M5.Lcd.setCursor(0, 6, 2);
      M5.Lcd.setTextColor(WHITE, BLACK);
      M5.Lcd.setTextSize(2);
      M5.Lcd.printf("Wifi is OFF");
    }
  }
  esp_sleep_enable_timer_wakeup(TIME_TO_SLEEP * uS_TO_S_FACTOR);
  Serial.println("ESP32 is going to sleep 60 secods...");
  M5.Lcd.fillScreen(BLACK);//Clear screen for the new message
  M5.Lcd.setCursor(0, 6, 2);
  M5.Lcd.setTextColor(WHITE, BLACK);
  M5.Lcd.setTextSize(2);
  M5.Lcd.printf("Sleeping...");
  M5.Lcd.fillScreen(BLACK);
  Serial.flush();
  esp_deep_sleep_start();
}

void saveCredentials(){
  EEPROM.begin(512);
  EEPROM.put(0, ssid);
  EEPROM.put(0 + sizeof(ssid), password);
  EEPROM.put(0 + sizeof(ssid) + sizeof(password), serverName);
  char ok[2 + 1] = "OK";
  EEPROM.put(0 + sizeof(ssid) + sizeof(password) + sizeof(serverName), ok);
  EEPROM.commit();
  EEPROM.end();
}

bool loadCredentials(){
  bool loaded = true;
  EEPROM.begin(512);
  EEPROM.get(0, ssid);
  EEPROM.get(0 + sizeof(ssid), password);
  EEPROM.get(0 + sizeof(ssid) + sizeof(password), serverName);
  char ok[2 + 1];
  EEPROM.get(0 + sizeof(ssid) + sizeof(password) + sizeof(serverName), ok);
  EEPROM.end();
  if(String(ok) != String("OK")){
    ssid[0] = 0;
    password[0] = 0;
    loaded = false;
  }
  Serial.print("Recovered credentials: ");
  Serial.print(ssid);
  Serial.print(", ");
  Serial.println(password);
  Serial.print("SERVER NAME: ");
  Serial.println(serverName);
  EEPROM.end();
  return loaded;
}

void setup() {
  Wire.begin();
  Serial.begin(115200);
  M5.begin();
  M5.Lcd.setRotation(3);

  if(loadCredentials()){
    //If there are credentials stored in EEPROM
    Serial.print("Connectiong to ");
    Serial.println(ssid);
    wifiDisconnect();
    wifiConnect(15);
    if(wifiStatus){
      //WiFi Credentials are correct
      Serial.println("");
      Serial.print("Connected to WiFi Network with IP Address: ");
      Serial.println(WiFi.localIP());
      HTTPClient http;
      http.begin(serverName);
      int response = http.GET();
      if(response == 200){
        http.end();
        //Server name is correct
        startSensor();
      }else{
        startCaptivePortal();
        portalStarted = true;
      }     
    }else{
      startCaptivePortal();
      portalStarted = true;
    }    
  }else{
    //No credentials, then start Captive Portal
    startCaptivePortal();
    portalStarted = true;
  }
}

void loop() {
  if(portalStarted){
    dnsServer.processNextRequest();
    webServer.handleClient();   
  } 
}
