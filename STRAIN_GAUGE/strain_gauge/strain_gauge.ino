void setup()
{
  Serial.begin(9600);
}

// GND    VCC     OUT
// BROWN  RED    ORANGE
// VIOLET WHITE  GRAY

void loop()
{
  float time = micros() / 1e6;
  int raw_analog_value = analogRead(A0);
  unsigned int sample_count = 15;
  float average_value = 0;
  for (int i = 0; i < sample_count ; i++){
    average_value += analogRead(A0);
    delay(1);
  }
  average_value = average_value / sample_count;  
  double voltage = (average_value/1024.0)*5.0;

  Serial.print(time);
  Serial.print(", ");
  Serial.print(raw_analog_value);
  Serial.print(",");
  Serial.print(average_value);
  Serial.print(",");
  Serial.println(voltage);
  delay(100);
}

