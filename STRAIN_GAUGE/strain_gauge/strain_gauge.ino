void setup() {
  Serial.begin(115200);
}

void loop() {
  float time = micros()/1e6;

  int sensorValue = 1024 - analogRead(A0) - 2.5;
  double volts = ((float)sensorValue / 1024) * 5;
  double mStrain = volts*1000/2;
  delay(100);
  Serial.print(time);
  Serial.print(", ");
  Serial.print(sensorValue);
  Serial.print(", ");
  Serial.print(volts);
  Serial.print(", ");
  Serial.println(mStrain);



  // x / 5 = sens_count / 1024

  // x = (sens_count / 1024) * 5
}
