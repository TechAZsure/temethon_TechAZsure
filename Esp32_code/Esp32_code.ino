#include <WiFi.h>
#include <FirebaseESP32.h>
#include <OneWire.h>
#include <DallasTemperature.h>
#include <BlynkSimpleEsp32.h>

// ------------------------
// WiFi Configuration
// ------------------------
#define WIFI_SSID       "TechAZsure"
#define WIFI_PASSWORD   "TeChAzSuRe786"

// ------------------------
// Firebase Configuration
// ------------------------
#define FIREBASE_HOST   "https://temenos-techazsure-default-rtdb.asia-southeast1.firebasedatabase.app/"
#define FIREBASE_AUTH   "DTx3aoOZVsOFu20cVnqTbcymuOEKN78FB2mj6QD3"

// ------------------------
// Blynk Configuration
// ------------------------
#define BLYNK_AUTH_TOKEN "x1OxW41lXyGwodq4L_cX71-c8S0cuHUm"

// ------------------------
// Sensor Pin Definitions
// ------------------------
#define CO2_SENSOR_PIN         36  // Example: GPIO36 for CO₂ analog sensor
#define VOLTAGE_SENSOR1_PIN    32  // Example: GPIO32 for voltage sensor 1
#define VOLTAGE_SENSOR2_PIN    33  // Example: GPIO33 for voltage sensor 2
#define CURRENT_SENSOR1_PIN    34  // Example: GPIO34 for current sensor 1
#define CURRENT_SENSOR2_PIN    35  // Example: GPIO35 for current sensor 2
#define ONE_WIRE_BUS            4  // Example: GPIO4 for DS18B20 sensors

// ------------------------
// Initialize DS18B20 Sensors
// ------------------------
OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature ds18b20Sensors(&oneWire);

// ------------------------
// Initialize Firebase Data object
// ------------------------
FirebaseData firebaseData;

// ------------------------
// Timing Variables for Periodic Updates
// ------------------------
unsigned long previousMillis = 0;
const long interval = 5000;  // Update every 5 seconds

// ------------------------
// Setup Function
// ------------------------
void setup() {
  Serial.begin(115200);
  
  // Connect to WiFi
  Serial.print("Connecting to WiFi");
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println();
  Serial.print("Connected! IP Address: ");
  Serial.println(WiFi.localIP());

  // Initialize Firebase
  Firebase.begin(FIREBASE_HOST, FIREBASE_AUTH);

  // Initialize DS18B20 sensors
  ds18b20Sensors.begin();

  // Initialize Blynk
  Blynk.begin(BLYNK_AUTH_TOKEN, WIFI_SSID, WIFI_PASSWORD);
}

// ------------------------
// Main Loop Function
// ------------------------
void loop() {
  // Run Blynk tasks
  Blynk.run();

  // Update sensor data every 'interval' milliseconds
  unsigned long currentMillis = millis();
  if (currentMillis - previousMillis >= interval) {
    previousMillis = currentMillis;
    
    // ------------------------
    // Read Sensor Data
    // ------------------------
    
    // CO₂ sensor reading (raw ADC value; convert if needed)
    int co2Raw = analogRead(CO2_SENSOR_PIN);
    float co2Value = (float)co2Raw;  // Conversion can be applied here

    // Voltage sensor readings
    int voltageRaw1 = analogRead(VOLTAGE_SENSOR1_PIN);
    int voltageRaw2 = analogRead(VOLTAGE_SENSOR2_PIN);
    float voltage1 = (float)voltageRaw1;  // Apply conversion if needed
    float voltage2 = (float)voltageRaw2;  // Apply conversion if needed

    // Current sensor readings
    int currentRaw1 = analogRead(CURRENT_SENSOR1_PIN);
    int currentRaw2 = analogRead(CURRENT_SENSOR2_PIN);
    float current1 = (float)currentRaw1;  // Apply conversion if needed
    float current2 = (float)currentRaw2;  // Apply conversion if needed

    // Temperature sensor readings (DS18B20)
    ds18b20Sensors.requestTemperatures(); // Initiate temperature conversion
    float temperature1 = ds18b20Sensors.getTempCByIndex(0); // First DS18B20
    float temperature2 = ds18b20Sensors.getTempCByIndex(1); // Second DS18B20

    // ------------------------
    // Debug: Print Sensor Data to Serial Monitor
    // ------------------------
    Serial.print("CO₂: "); Serial.print(co2Value);
    Serial.print(" | Voltage1: "); Serial.print(voltage1);
    Serial.print(" | Voltage2: "); Serial.print(voltage2);
    Serial.print(" | Current1: "); Serial.print(current1);
    Serial.print(" | Current2: "); Serial.print(current2);
    Serial.print(" | Temp1: "); Serial.print(temperature1);
    Serial.print(" | Temp2: "); Serial.println(temperature2);

    // ------------------------
    // Push Data to Firebase (updates same keys every cycle)
    // ------------------------
    Firebase.setFloat(firebaseData, "/sensor_data/co2", co2Value);
    Firebase.setFloat(firebaseData, "/sensor_data/voltage1", voltage1);
    Firebase.setFloat(firebaseData, "/sensor_data/voltage2", voltage2);
    Firebase.setFloat(firebaseData, "/sensor_data/current1", current1);
    Firebase.setFloat(firebaseData, "/sensor_data/current2", current2);
    Firebase.setFloat(firebaseData, "/sensor_data/temperature1", temperature1);
    Firebase.setFloat(firebaseData, "/sensor_data/temperature2", temperature2);

    // ------------------------
    // Push Data to Blynk
    // ------------------------
    // Use Virtual Pins for your Blynk widgets (e.g., gauges, LCD)
    // Update gauge widgets:
    Blynk.virtualWrite(V0, co2Value);         // Gauge for CO₂
    Blynk.virtualWrite(V1, voltage1);         // Gauge for Voltage Sensor 1
    Blynk.virtualWrite(V2, voltage2);         // Gauge for Voltage Sensor 2
    Blynk.virtualWrite(V3, current1);         // Gauge for Current Sensor 1
    Blynk.virtualWrite(V4, current2);         // Gauge for Current Sensor 2
    Blynk.virtualWrite(V5, temperature1);     // Gauge for Temperature Sensor 1
    Blynk.virtualWrite(V6, temperature2);     // Gauge for Temperature Sensor 2

    // Example: Update an LCD widget (if using one) on Virtual Pin V7:
    // The LCD widget on Blynk can display multiple lines. For instance:
    String lcdText = "CO2:" + String(co2Value) + "\n" +
                     "V1:" + String(voltage1) + " V";
    Blynk.virtualWrite(V7, lcdText);
  }
}
