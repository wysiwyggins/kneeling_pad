// Constructor
BLEHidAdafruit(void);

// Call this once to start the HID service
virtual err_t begin(void);

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);

  Serial.println("Bluefruit52 HID Keyboard Example");

  Bluefruit.begin();
  Bluefruit.setName("Kids_Genuflector");

  // Config and Start Device Information Service

}

void loop() {
  // put your main code here, to run repeatedly:

}
