/*********************************************************************
 This is an example for our nRF52 based Bluefruit LE modules

 Pick one up today in the adafruit shop!

 Adafruit invests time and resources providing this open source code,
 please support Adafruit and open-source hardware by purchasing
 products from Adafruit!

 MIT license, check LICENSE for more information
 All text above, and the splash screen below must be included in
 any redistribution
*********************************************************************/
#include <bluefruit.h>
#include <BLE52_Mouse_and_Keyboard.h>

BLEDis bledis;
BLEHidAdafruit blehid;

const int ATARI_ORANGE = A0;
const int ATARI_GREEN = A1;
const int ATARI_BROWN = A2;
const int ATARI_WHITE = A3;
const int ATARI_BLUE = A4;
const int KNEELER = A5;
const int LED_PIN = 13;

bool Mouse.isConnected(void);
bool Keyboard.isConnected(void);

bool hasKeyPressed = false;





void setup() 
{

  //pins
  pinMode(ATARI_ORANGE, INPUT_PULLUP);
  pinMode(ATARI_GREEN, INPUT_PULLUP);
  pinMode(ATARI_BROWN, INPUT_PULLUP);
  pinMode(ATARI_WHITE, INPUT_PULLUP);
  pinMode(KNEELER, INPUT_PULLUP);
  pinMode(LED_PIN, OUTPUT);
  
  //Bluetooth
  Serial.begin(115200);
  while ( !Serial ) delay(10);   // for nrf52840 with native usb

  Serial.println("Bluefruit52 HID Keyboard Example");
  Serial.println("--------------------------------\n");

  Serial.println();
  Serial.println("Go to your phone's Bluetooth settings to pair your device");
  Serial.println("then open an application that accepts keyboard input");

  Serial.println();
  Serial.println("Enter the character(s) to send:");
  Serial.println();  

  Bluefruit.begin();
  Bluefruit.setTxPower(4);    // Check bluefruit.h for supported values

  // Configure and Start Device Information Service
  bledis.setManufacturer("Adafruit Industries");
  bledis.setModel("Bluefruit Feather 52");
  bledis.begin();

  /* Start BLE HID
   * Note: Apple requires BLE device must have min connection interval >= 20m
   * ( The smaller the connection interval the faster we could send data).
   * However for HID and MIDI device, Apple could accept min connection interval 
   * up to 11.25 ms. Therefore BLEHidAdafruit::begin() will try to set the min and max
   * connection interval to 11.25  ms and 15 ms respectively for best performance.
   */
  blehid.begin();

  // Set callback for set LED from central
  blehid.setKeyboardLedCallback(set_keyboard_led);

  /* Set connection interval (min, max) to your perferred value.
   * Note: It is already set by BLEHidAdafruit::begin() to 11.25ms - 15ms
   * min = 9*1.25=11.25 ms, max = 12*1.25= 15 ms 
   */
  /* Bluefruit.Periph.setConnInterval(9, 12); */

  // Set up and start advertising
  startAdv();
}

void startAdv(void)
{  
  // Advertising packet
  Bluefruit.Advertising.addFlags(BLE_GAP_ADV_FLAGS_LE_ONLY_GENERAL_DISC_MODE);
  Bluefruit.Advertising.addTxPower();
  Bluefruit.Advertising.addAppearance(BLE_APPEARANCE_HID_KEYBOARD);
  
  // Include BLE HID service
  Bluefruit.Advertising.addService(blehid);

  // There is enough room for the dev name in the advertising packet
  Bluefruit.Advertising.addName();
  
  /* Start Advertising
   * - Enable auto advertising if disconnected
   * - Interval:  fast mode = 20 ms, slow mode = 152.5 ms
   * - Timeout for fast mode is 30 seconds
   * - Start(timeout) with timeout = 0 will advertise forever (until connected)
   * 
   * For recommended advertising interval
   * https://developer.apple.com/library/content/qa/qa1931/_index.html   
   */
  Bluefruit.Advertising.restartOnDisconnect(true);
  Bluefruit.Advertising.setInterval(32, 244);    // in unit of 0.625 ms
  Bluefruit.Advertising.setFastTimeout(30);      // number of seconds in fast mode
  Bluefruit.Advertising.start(0);                // 0 = Don't stop advertising after n seconds
}

void loop() 
{


  int fire = digitalRead(ATARI_ORANGE);
  int up = digitalRead(ATARI_GREEN);
  int down = digitalRead(ATARI_BROWN);
  int left = digitalRead(ATARI_WHITE);
  int right = digitalRead(ATARI_BLUE);
  int kneel = digitalRead(KNEELER);

  // from circuitpython version
  
  while (true) {
    Keyboard.begin();
    if (fire == LOW){
      Keyboard.press(KEY_RETURN);
    } else if (up == LOW){
      Keyboard.press(KEY_UP_ARROW);
    } else if (down == LOW) {
      Keyboard.press(KEY_DOWN_ARROW)
    } else if (left == LOW){
      Keyboard.press(KEY_LEFT_ARROW)
    } else if (right == LOW){
      Keyboard.press(KEY_RIGHT_ARROW)
    } else if (kneel == LOW) {
      Keyboard.press('p');
    } 
    delay(10);
  }

  // from bluefruit hid keyboard example
  
  // Only send KeyRelease if previously pressed to avoid sending
  // multiple keyRelease reports (that consume memory and bandwidth)
  if ( hasKeyPressed )
  {
    hasKeyPressed = false;
    blehid.keyRelease();
    
    // Delay a bit after a report
    delay(5);
  }
    
  if (Serial.available())
  {
    char ch = (char) Serial.read();

    // echo
    Serial.write(ch); 

    blehid.keyPress(ch);
    hasKeyPressed = true;
    
    // Delay a bit after a report
    delay(5);
  }
}

/**
 * Callback invoked when received Set LED from central.
 * Must be set previously with setKeyboardLedCallback()
 *
 * The LED bit map is as follows: (also defined by KEYBOARD_LED_* )
 *    Kana (4) | Compose (3) | ScrollLock (2) | CapsLock (1) | Numlock (0)
 */
void set_keyboard_led(uint16_t conn_handle, uint8_t led_bitmap)
{
  (void) conn_handle;
  
  // light up Red Led if any bits is set
  if ( led_bitmap )
  {
    ledOn( LED_RED );
  }
  else
  {
    ledOff( LED_RED );
  }
}
