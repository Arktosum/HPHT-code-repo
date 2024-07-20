void setup()
{
  Serial.begin(115200);
}
void loop()
{
  float time = micros() / 1e6;
  float drift = 4.5; // 7.0; 
  int rawAnalogValue = analogRead(A0);
  int analogValue = 1022-rawAnalogValue - drift;
  double volts = ((double)analogValue / 1022)*5;
  double mStrain = volts*500; // 0 - 2500 microStrain
  Serial.print(time);
  Serial.print(", ");
  // Serial.print(rawAnalogValue);
  // Serial.print(", ");
  Serial.print(analogValue);
  Serial.print(", ");
  Serial.print(volts);
  Serial.print(", ");
  Serial.println(mStrain);
  delay(50);
}

