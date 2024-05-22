void setup() {
  Serial.begin(115200);
}

void loop() {
  float time = micros()/1e6;

  int sensorValue = analogRead(A0);
  delay(100);

  Serial.print(time);
  Serial.print(", ");
  Serial.println(sensorValue);
}
