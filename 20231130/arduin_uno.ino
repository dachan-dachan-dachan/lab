//https://qiita.com/ryota765/items/0cfc2ea2d598de11b174

float sensorValue = 0;
//int sensorValue = 0;
int delay_time = 100;//ms

void setup() {
  Serial.begin(9600);
}

void loop() {
  sensorValue = analogRead(A0);
  Serial.println(sensorValue);
  
  delay(delay_time);
}
