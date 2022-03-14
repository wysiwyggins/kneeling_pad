/*
 * Sample program demonstrating BLE52_Mouse_and_Keyboard.h module which
 * simulates the standard Arduino Mouse.h API and Arduino Keyboard.h API 
 * for use with Bluetooth connections with the nRF52840.
 * This program tests the keyboard portion alone.
 */
#include <bluefruit.h>
#include <BLE52_Mouse_and_Keyboard.h>

uint8_t Multiple[3]= {'1','2','3'};

const int ATARI_ORANGE = A0;
const int ATARI_GREEN = A1;
const int ATARI_BROWN = A2;
const int ATARI_WHITE = A3;
const int ATARI_BLUE = A4;
const int KNEELER = A5;
const int LED_PIN = 13;

void setup() 
{


  //pins
  pinMode(ATARI_ORANGE, INPUT_PULLUP);
  pinMode(ATARI_GREEN, INPUT_PULLUP);
  pinMode(ATARI_BROWN, INPUT_PULLUP);
  pinMode(ATARI_WHITE, INPUT_PULLUP);
  pinMode(KNEELER, INPUT_PULLUP);
  pinMode(LED_PIN, OUTPUT);

  //bluetooth
  
  Serial.begin(115200);
  while ( !Serial ) delay(10);   // for nrf52840 with native usb
  Serial.println("Bluefruit52 HID Keyboard Example");
  Serial.println("Go to your phone's Bluetooth settings to pair your device");
  Serial.println("then open an application that accepts keyboard input");

  Keyboard.begin();  //Unlike the standard Keyboard.h you MUST use the "Keyboard.begin();" method
  Serial.print("Attempting to connect");
  uint8_t i=0;
  while(! Keyboard.isConnected()) { 
    Serial.print("."); delay(100);
    if((++i)>50) {
      i=0; Serial.println();
    }
  };
  delay(1000);//just in case
  Serial.println("\nConnection successful");
//  
//  Keyboard.write('a');            //press and release 'a' key
//  Keyboard.write(Multiple,3);     //multiple keys sequentially from a buffer
//  Keyboard.print("456");          //print a string
//  Keyboard.println("789");        //print another string with a line
//  Keyboard.press(KEY_LEFT_SHIFT); //hold down the shift
//  Keyboard.println("a uppercase sentence"); //this will be all caps
//  Keyboard.release(KEY_LEFT_SHIFT);//release the shift
//  Keyboard.println ("back to lowercase");
//  Keyboard.press(KEY_LEFT_SHIFT); //press shift
//  Keyboard.println("1234");       //some text
//  Keyboard.releaseAll();          //release all
//  Keyboard.println("1234");       //not shifted
//  Keyboard.print("A mistake");  //will attempt to erase this
//  delay(1000);
//  Keyboard.press(KEY_LEFT_CTRL);  //will attempt control-z
//  Keyboard.write('z');
//  Keyboard.releaseAll();         //release the control key
//  Serial.println("USB keyboard test completed.\n");
};
void loop() {

    int fire = digitalRead(ATARI_ORANGE);
    int up = digitalRead(ATARI_GREEN);
    int down = digitalRead(ATARI_BROWN);
    int left = digitalRead(ATARI_WHITE);
    int right = digitalRead(ATARI_BLUE);
    int kneel = digitalRead(KNEELER);
  
    while (true) {
      if (fire == LOW) {
        Keyboard.write(KEY_RETURN);
      } else if (up == LOW) {
        Keyboard.write(KEY_UP_ARROW);
      } else if (down == LOW) {
        Keyboard.write(KEY_DOWN_ARROW);
      } else if (left == LOW) {
        Keyboard.write(KEY_LEFT_ARROW);
      } else if (right == LOW) {
        Keyboard.write(KEY_RIGHT_ARROW);
      } else if (kneel == LOW) {
        Keyboard.press('p');
        Serial.println("kneeling.\n");
      } 
      delay(10);
    }
}

/*
 * Click below before uploading and it will type characters in this comment
 * 
 * 
 * 
 * 
 * 
 *  
 *  
 *  
 *  
 *  
 *  
 */
