#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <Servo.h>

LiquidCrystal_I2C lcd(0x27, 16, 2); // change to 0x3F if needed

Servo thumb, indexF, middleF, ringF, pinky;
String letter = "";

void setup() {
  Serial.begin(115200);

  lcd.init();
  lcd.backlight();
  lcd.setCursor(0,0);
  lcd.print("HELLO");

  thumb.attach(5);
  indexF.attach(6);
  middleF.attach(9);
  ringF.attach(10);
  pinky.attach(11);

  openHand();
}

void loop() {
  if (Serial.available()) {
    letter = Serial.readStringUntil('\n');
    letter.trim();

    lcd.clear();
    lcd.setCursor(0,0);
    lcd.print("Letter:");
    lcd.setCursor(0,1);
    lcd.print(letter);

    if (letter == "A") {
      signA();
    }
    else if (letter == "B") {
      signB();
    }
    else if (letter == "D") {
      signD();
    }
    else if (letter == "F") {
      signF();
    }
    else if (letter == "I") {
      signI();
    }
    else if (letter == "L") {
      signL();
    }
    else if (letter == "S") {
      signS();
    }
    else if (letter == "V") {
      signV();
    }
    else if (letter == "W") {
      signW();
    }
    else if (letter == "Y") {
      signY();
    }
  }
}

/* -------- HAND POSITIONS -------- */

void openHand() {
  thumb.write(0);
  indexF.write(0);
  middleF.write(0);
  ringF.write(0);
  pinky.write(0);
}

// ASL A: thumb UP, others DOWN
void signA() {
  thumb.write(0);
  indexF.write(180);
  middleF.write(180);
  ringF.write(180);
  pinky.write(180);
}

// ASL B: thumb DOWN, others UP
void signB() {
  thumb.write(180);
  indexF.write(0);
  middleF.write(0);
  ringF.write(0);
  pinky.write(0);
}
// ASL D: index UP, others DOWN
void signD() {
  thumb.write(180);
  indexF.write(0);
  middleF.write(180);
  ringF.write(180);
  pinky.write(180);
}
// ASL F: index thumb down, others UP
void signF() {
  thumb.write(180);
  indexF.write(180);
  middleF.write(0);
  ringF.write(0);
  pinky.write(0);
}
// ASL I: pinkey Up, others DOWN
void signI() {
  thumb.write(180);
  indexF.write(180);
  middleF.write(180);
  ringF.write(180);
  pinky.write(0);
}
// ASL L: index thumb UP, others DOWN
void signL() {
  thumb.write(0);
  indexF.write(0);
  middleF.write(180);
  ringF.write(180);
  pinky.write(180);
}
// ASL S: all finger Down
void signS() {
  thumb.write(180);
  indexF.write(180);
  middleF.write(180);
  ringF.write(180);
  pinky.write(180);
}
// ASL V: middle index UP,others DOWN
void signV() {
  thumb.write(0);
  indexF.write(0);
  middleF.write(180);
  ringF.write(180);
  pinky.write(180);
}
// ASL W: ring middle index UP , others DOWN
void signW() {
  thumb.write(180);
  indexF.write(0);
  middleF.write(0);
  ringF.write(0);
  pinky.write(180);
}
// ASL Y: pinkey thumb UP,others DOWN
void signY() {
  thumb.write(0);
  indexF.write(180);
  middleF.write(180);
  ringF.write(180);
  pinky.write(0);
}