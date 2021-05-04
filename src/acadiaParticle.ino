// Import libraries

#include <Adafruit_GPS.h>
#include <SPI.h>
#include <SD.h>
// #include <iostream>
// #include <string>

// Set whether you want the device to publish data to the internet by default here.
// 1 will Particle.publish AND Serial.print, 0 will just Serial.print
// Extremely useful for saving data while developing close enough to have a cable plugged in.
// You can also change this remotely using the Particle.function "tmode" defined in setup()
//int transmittingData = 1;

// Used to keep track of the last time we published data
//long lastPublish = 0;

SYSTEM_THREAD(ENABLED);

// How many minutes between publishes? 10+ recommended for long-time continuous publishing!
//int delayMinutes = 10;
#define GPSECHO false
#define GPSSerial Serial1
Adafruit_GPS GPS(&GPSSerial);

FuelGauge fuel;
uint32_t timer = millis();
File logfile;
File CDalt;

const pin_t cut = D7;
const pin_t safe = D8;
const int cardSelect = 5;
String GPS_fix_string;
String SDCardInit;
String tempCDalt;
String flightMode;
double lat;
double lon;
double alt;
double battVolt;
int cutDownAlt;
int SDstartup;


void setup() {
  Serial.begin(115200);
  delay(2000);
  Serial.println("Acadia Flight Computer is in startup...");
  SDstartup = 0;

  // Set up Particle OS functions/variables
  Particle.function("cutDown", cutDown);
  Particle.function("safeCutDown", safeCutDown);
  Particle.function("setCutDownAlt", setCutDownAlt);
  Particle.function("setFlightMode", setFlightMode);
  Particle.variable("GPSfix", GPS_fix_string);
  Particle.variable("SDCardInit", SDCardInit);
  Particle.variable("Latitude", lat);
  Particle.variable("Longitude", lon);
  Particle.variable("Altitude (m)", alt);
  Particle.variable("Battery Voltage", battVolt);
  Particle.variable("CutDownAlt (m)", cutDownAlt);

  
  // Set up the GPS module
  GPS.begin(9600);
  GPS.sendCommand(PMTK_SET_NMEA_OUTPUT_RMCGGA);
  GPS.sendCommand(PMTK_SET_NMEA_UPDATE_1HZ);
  GPS.sendCommand(PGCMD_ANTENNA);
  delay(1000);
  GPSSerial.println(PMTK_Q_RELEASE);
  Serial.println("Pausing...");
  delay(10000);

  // see if the card is present and can be initialized:
  while (SDstartup < 10)
  {
    if (!SD.begin(cardSelect)) {
      Serial.println("Card initializing...");
      SDCardInit = "Failed";
      delay(1000);
    }
    else
    {
      Serial.println("Card init. success!");
      SDCardInit = "Success";
      SDstartup = 20;
    }
    SDstartup++;
  }

  // Set cutdown control pins to output 
  pinMode(safe, OUTPUT);
  pinMode(cut, OUTPUT);
  digitalWrite(safe, HIGH);
  delay(1000);
  digitalWrite(safe, LOW);


  // set default values in case of restart midflight
  cutDownAlt = 100;
  flightMode = "flight";
  Serial.println("Ready!");
}

void loop() {
  // read data from the GPS in the 'main loop'
  char c = GPS.read();

  if (GPS.newNMEAreceived()) {
    if (!GPS.parse(GPS.lastNMEA()))
      return;
  }
  // Approximately every 2 seconds or so, print out the current stats
  if (millis() - timer > 10000) {
    timer = millis(); // reset the timer
    Serial.print("\nBattery Voltage:");
    Serial.println(fuel.getVCell());
    battVolt = fuel.getVCell();
    Serial.print("\nTime: ");
    if (GPS.hour < 10) { Serial.print('0'); }
    Serial.print(GPS.hour, DEC); Serial.print(':');
    if (GPS.minute < 10) { Serial.print('0'); }
    Serial.print(GPS.minute, DEC); Serial.print(':');
    if (GPS.seconds < 10) { Serial.print('0'); }
    Serial.print(GPS.seconds, DEC); Serial.print('.');
    if (GPS.milliseconds < 10) {
      Serial.print("00");
    } else if (GPS.milliseconds > 9 && GPS.milliseconds < 100) {
      Serial.print("0");
    }
    Serial.println(GPS.milliseconds);
    Serial.print("Date: ");
    Serial.print(GPS.day, DEC); Serial.print('/');
    Serial.print(GPS.month, DEC); Serial.print("/20");
    Serial.println(GPS.year, DEC);
    Serial.print("Fix: "); Serial.print((int)GPS.fix);
    Serial.print(" quality: "); Serial.println((int)GPS.fixquality);
    if (GPS.fix) {
      GPS_fix_string = "Good GPS Fix";
      Serial.print("Location: ");
      Serial.print(GPS.latitudeDegrees, 8); //Serial.println(GPS.lat);
      Serial.print(", ");
      Serial.println(GPS.longitudeDegrees, 8); //Serial.println(GPS.lon);
      Serial.print("Speed (knots): "); Serial.println(GPS.speed);
      Serial.print("Altitude: "); Serial.println(GPS.altitude);
      Serial.print("Satellites: "); Serial.println((int)GPS.satellites);
      lat = GPS.latitudeDegrees;
      lon = GPS.longitudeDegrees;
      alt = GPS.altitude;

      if (flightMode.equals("flight"))
      {
        if (alt > cutDownAlt){
          Serial.println("above burst altitude!");
          digitalWrite(cut, HIGH);
          delay(1000);
          digitalWrite(cut, LOW);
        } else{
          digitalWrite(safe, HIGH);
          delay(1000);
          digitalWrite(safe, LOW);
        }
      }
    }
    else
    {
      GPS_fix_string = "No GPS Fix";
    }
    logfile = SD.open("datalog.txt", FILE_WRITE);
    logfile.print("Time: "); logfile.print(GPS.hour); logfile.print(':');
    logfile.print(GPS.minute, DEC); logfile.print(':'); logfile.println(GPS.seconds, DEC);
    logfile.print("Postion: "); logfile.print(GPS.latitudeDegrees, 6);
    logfile.print(", "); logfile.println(GPS.longitudeDegrees, 6);
    logfile.print("Altitude: "); logfile.println(GPS.altitude);
    logfile.print("Satellites: "); logfile.println(GPS.satellites);
    logfile.print("Battery Voltage: "); logfile.println(fuel.getVCell());
    logfile.println(" ");
    logfile.close();

  }
}


int cutDown(String command)
{
  if (command.equals("go"))
  {
    digitalWrite(cut, HIGH);
    delay(1000);
    digitalWrite(cut, LOW);
    return 1;
  }
  else
  {
    return -1;
  }
}

int safeCutDown(String command)
{
  if (command.equals("go"))
  {
    digitalWrite(safe, HIGH);
    delay(1000);
    digitalWrite(safe, LOW);
    return 1;
  }
  else
  {
    return -1;
  }
}

int setFlightMode(String command)
{
  if (command.equals("flight"))
  {
    flightMode = "flight";
    return 1;
  }
  else if (command.equals("testing"))
  {
    flightMode = "testing";
    return 1;
  }
  else
  {
    return -1;
  }
}

int setCutDownAlt(String command)
{
  cutDownAlt = command.toInt();
  return 1;
}


