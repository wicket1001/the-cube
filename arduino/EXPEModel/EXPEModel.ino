#include <Adafruit_NeoPixel.h>

//  0 GRID <-> Panel
//  1 BATTERIE <-> Panel
//  2 PV -> Panel
//  3 WIND -> Panel
//  4 SolarThermal / Water -> Panel
//  5 Attic right
//  6 Attic left
//  7 UP Attic
//  8 Third right
//  9 Third left
// 10 UP Third
// 11 Second right
// 12 Second left
// 13 UP Second
// 14 First right
// 15 First left
// 16 HeatPump <-> Panel
// 17 ThermalBattery <-> Panel
// 18 ThermalBattery <-> WaterBuffer
// 19 HeatPump <-> WaterBuffer
// 20 UP First Radiators <-> WaterBuffer
// 21 Radiators First
// 22 UP Second Radiators
// 23 Radiators Second
// 24 UP Third Radiators
// 25 Radiators Third
// 26 ---

#define SEGMENTS 26
int pin = 5;                // input pin Neopixel is attached to
int totalNum = 350;         // number of neopixels in whole strip
unsigned long currentTime;  // running time for program
int redColors[SEGMENTS] = {255, 255, 0, 0, 0, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255};
int greenColors[SEGMENTS] = {0, 200, 255, 255, 255, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 0, 0, 0, 0, 0, 0, 0, 0};
int blueColors[SEGMENTS] = {255, 0, 255, 255, 255, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
int directions[SEGMENTS] = {1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1};
int intervals[SEGMENTS] = {20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20};
bool newPeriods[SEGMENTS] = {true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true};
unsigned long periodStarts[SEGMENTS] = {};
int numLEDS[SEGMENTS] = {5, 7, 35, 34, 36, 9, 9, 6, 9, 9, 6, 9, 9, 6, 9, 9, 16, 8, 7, 6, 3, 20, 7, 20, 8, 20};
int firstIndices[SEGMENTS] = {0, 11, 46, 47, 116, 125, 126, 140, 149, 150, 164, 173, 174, 188, 197, 198, 222, 223, 231, 238, 244, 247, 267, 274, 292, 300};
int currentIndices[SEGMENTS] = {0, 11, 46, 47, 116, 125, 126, 140, 149, 150, 164, 173, 174, 188, 197, 198, 222, 223, 231, 238, 244, 247, 267, 274, 292, 300};
int prevIndices[SEGMENTS] = {100, 100, 100, 100, 200, 200, 200, 200, 200, 200, 200, 300, 300, 300, 300, 300, 300, 300, 300, 300, 300, 300, 300, 300, 300, 300};

Adafruit_NeoPixel pixels = Adafruit_NeoPixel(totalNum, pin, NEO_GRB + NEO_KHZ800);

int forwardBlink(int start, int N, int prevN, int num, int red, int green, int blue) {
  prevN = N - 1;
  if (N == start && currentTime > 0) {
    prevN = start + num - 1;
  }
  LED_move(prevN, N, red, green, blue);
  N++;
  if (N == num + start) {
    N = start;
  }
  return N;
}


int backwardBlink(int start, int N, int prevN, int num, int red, int green, int blue) {
  prevN = N + 1;
  if (N == start && currentTime > 0) {
    prevN = start - num + 1;
  }
  LED_move(prevN, N, red, green, blue);
  N--;
  if (N == start - num) {
    N = start;
  }
  return N;
}

void LED_move(int prevN, int N, int red, int green, int blue) {
  pixels.setPixelColor(N, pixels.Color(red, green, blue));
  pixels.setPixelColor(prevN, pixels.Color(0, 0, 0));
  //pixels.show();
}

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  // Initialize the NeoPixel library.
  pixels.begin();
  for (int i = 0; i < SEGMENTS; i++) {
    pixels.setPixelColor(firstIndices[i], pixels.Color(redColors[i], greenColors[i], blueColors[i]));
  }
  // defineInterval();
}

void loop() {
  // put your main code here, to run repeatedly:
  currentTime = millis();
  for (int i = 0; i < SEGMENTS; i++) {
    if (newPeriods[i] == true) {
      periodStarts[i] = currentTime;
      newPeriods[i] = false;
    }
    if (currentTime - periodStarts[i] > intervals[i]) {
      if (directions[i] == 0) {
        currentIndices[i] = backwardBlink(firstIndices[i], currentIndices[i], prevIndices[i], numLEDS[i], redColors[i], greenColors[i], blueColors[i]);
      } else {
        currentIndices[i] = forwardBlink(firstIndices[i], currentIndices[i], prevIndices[i], numLEDS[i], redColors[i], greenColors[i], blueColors[i]);
      }
      newPeriods[i] = true;
    }
  }
  pixels.show();
}
