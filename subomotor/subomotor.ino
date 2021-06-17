#include <Servo.h>

Servo servo;
int value=0;

void setup()
{
  servo.attach(7);
  Serial.begin(9600);
  servo.write(103);
}

void loop()
{
  if(Serial.available())
  {
    int in_data;
    in_data = Serial.read();
    Serial.println(in_data);
    if(in_data == 48)
    {
      servo.write(30);
      delay(1000);
      servo.write(103);
    }
    else if (in_data == 49)
    {
     servo.write(170);
     delay(1000);
     servo.write(103);
    }
  }
}
