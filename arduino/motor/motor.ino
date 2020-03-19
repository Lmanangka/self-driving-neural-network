#include <Wire.h>

#define IN1 11
#define IN2 10
#define IN3 9
#define IN4 6

#define address 0x04

int x = 0;

void setup() {
  // put your setup code here, to run once:
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);

  Wire.begin(address);
  Wire.onReceive(receive);
  Serial.begin(9600);

}

void loop() {
  // put your main code here, to run repeatedly:

}

void receive(int byteCount) {
  while (Wire.available()) {
    x = Wire.read();
    //forward
    if (x == 0) {
      analogWrite(IN1, 0);
      analogWrite(IN2, 100);
      analogWrite(IN3, 100);
      analogWrite(IN4, 0);
    }
    //right
    else if (x == 1) {
      analogWrite(IN1, 150);
      analogWrite(IN2, 0);
      analogWrite(IN3, 150);
      analogWrite(IN4, 0);
    }
    //left
    else if (x == 2) {
      analogWrite(IN1, 0);
      analogWrite(IN2, 150);
      analogWrite(IN3, 0);
      analogWrite(IN4, 150);
    }
    //backward
    else if (x == 3) {
      analogWrite(IN1, 100);
      analogWrite(IN2, 0);
      analogWrite(IN3, 0);
      analogWrite(IN4, 100);
    }

    //stop
    else {
      analogWrite(IN1, 0);
      analogWrite(IN2, 0);
      analogWrite(IN3, 0);
      analogWrite(IN4, 0);
    }
  }
}
