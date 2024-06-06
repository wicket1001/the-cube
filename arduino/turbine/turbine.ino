int sensorValue = 0;
int outputValue = 1;
bool newPeriod = true;
unsigned long periodStart;
unsigned long currentTime;  // running time for program
int interval = 2000;

void setup() {
  pinMode(9, OUTPUT);
  Serial.begin(115200);
}

void loop() {
  currentTime = millis();
  if (newPeriod == true) {
    periodStart = currentTime;
    newPeriod = false;
  }
  if (currentTime - periodStart > interval) {
    if (outputValue == 1) {
      outputValue = 0;
              digitalWrite(9, 0);

    } else {
      outputValue = 1;
              digitalWrite(9, 1);
    }
          Serial.println(outputValue);
    newPeriod = true;
  }
}
