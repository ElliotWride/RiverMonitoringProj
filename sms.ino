
#include <SoftwareSerial.h>

// Configure software serial port
SoftwareSerial SIM900(7, 8); 

const int analogPhPin = A0; // PH module pin P0 connected to analog pin A0
long phTot;
float phAvg;
int x;
const float C = 7.4519; // Constant of straight line (Y = mx + C)
const float m = -0.155; // Slope of straight line (Y = mx + C)
// Pin Assignment and declaration end

// Global variables for ID, PH, and TIME
int ID = 123;          // Example ID
const char* TIME = "12:30";  // Example time

void setup() {
  // Arduino communicates with SIM900 GSM shield at a baud rate of 19200
  // Make sure that corresponds to the baud rate of your module
  SIM900.begin(19200);
  Serial.begin(9600);
  // Give time to your GSM shield log on to network
}

void loop() { 
  // Send pH reading every hour along with ID

  // Get pH readings
  phTot = 0;
  phAvg = 0;

  // Taking 10 samples and adding with 10 millisecond delay
  for(x=0; x<10 ; x++) {
    phTot += analogRead(A0);
    delay(10);
  }

  phAvg = phTot / 10;
  float phVoltage =  phAvg * (5.0 / 1023.0); // Convert sensor reading into millivolt
  float pHValue = phVoltage * m + C;

  // Output pH value to serial monitor
  Serial.print("pH Value: ");
  Serial.println(pHValue);
  // End get pH

  // Construct SMS message
  char sms[128] = "";

  char *tmpSign = (pHValue < 0) ? "-" : "";
  float tmpVal = (pHValue < 0) ? -pHValue : pHValue;

  int tmpInt1 = tmpVal;                  // Get the integer (678).
  float tmpFrac = tmpVal - tmpInt1;      // Get fraction (0.0123).
  int tmpInt2 = trunc(tmpFrac * 10000); 

  // Constructing SMS message format: "ID,PH,TIME"
  sprintf(sms, "%d,%s%d.%04d,%s", ID, tmpSign, tmpInt1, tmpInt2, TIME);
  Serial.println(sms);

  // Send constructed SMS
  sendSMS(sms);
  delay(600000 - 5400 - 100); // Corrected delay time make 10 mins
}

void sendSMS(char sms[128]) {
  // AT command to set SIM900 to SMS mode
  SIM900.print("AT+CMGF=1\r"); 
  delay(100);

  // REPLACE THE X's WITH THE RECIPIENT'S MOBILE NUMBER
  // USE INTERNATIONAL FORMAT CODE FOR MOBILE NUMBERS
  SIM900.println("AT+CMGS=\"+447873121158\""); 
  delay(100);
  
  // Send the constructed SMS
  SIM900.println(sms); // Sending the constructed message
  delay(100);

  // End AT command with a ^Z, ASCII code 26
  SIM900.println((char)26); 
  delay(100);
  
  // Give module time to send SMS
  delay(5000); 
}
