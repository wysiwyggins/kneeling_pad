const int ATARI_ORANGE = A0;
const int LED_PIN = 13;


// Call this once to start the HID service
virtual err_t begin(void);

void setup() {
  // put your setup code here, to run once:
  // buttons
  pinMode(LED_PIN, OUTPUT);
  pinMode(BUTTON_PIN, INPUT_PULLUP);

  // bluetooth
  Serial.begin(115200);

  Serial.println("Bluefruit52 HID Keyboard Example");

  Bluefruit.begin();
  Bluefruit.setName("Kids_Genuflector");

  // Config and Start Device Information Service
  bledis.setManufacturer("Adafruit Industries");
  bledis.setModel("Bluefruit Feather52");
  bledis.begin();
}

void loop() {
  // put your main code here, to run repeatedly:

  digitalWrite(13, HIGH);   // turn the LED on (HIGH is the voltage level)
  delay(1000);              // wait for a second
  digitalWrite(13, LOW);    // turn the LED off by making the voltage LOW
  delay(1000);
  
  int val = digitalRead(BUTTON_PIN);
 
  if (val == LOW) {
    digitalWrite(LED_PIN, HIGH);
  } else {
    digitalWrite(LED_PIN, LOW);
  }
}
