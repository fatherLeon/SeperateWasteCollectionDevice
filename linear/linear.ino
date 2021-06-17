int ENV=8;
int DIR=9;

void setup()
{
  Serial.begin(9600);
  pinMode(ENV, OUTPUT);
  pinMode(DIR, OUTPUT);
  digitalWrite(ENV, LOW);
  digitalWrite(DIR, LOW);
}

void loop()
{
  if(Serial.available())
  {
    int in_data;
    in_data = Serial.read();
    if (in_data == 49)
    {
      digitalWrite(ENV, LOW);
      digitalWrite(DIR, HIGH);
      delay(10000);
      digitalWrite(ENV, LOW);
      digitalWrite(DIR, LOW);
      delay(10000);
    }
  }
 }
