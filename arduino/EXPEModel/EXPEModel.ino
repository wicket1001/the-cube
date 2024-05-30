#include <Adafruit_NeoPixel.h>

int pin = 5;                // input pin Neopixel is attached to
int totalNum = 350;         // number of neopixels in whole strip
unsigned long currentTime;  // running time for program
int firstPixels[30] = {0, 11, 46, 47, 116, 125, 126, 140, 149, 150, 164, 173, 174, 188, 197, 198, 222, 223, 231, 238, 244, 248, 268, 275, 295, 302};
int redColors[30] = {255, 255, 0, 0, 0, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255};
int greenColors[30] = {0, 200, 255, 255, 255, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 0, 0, 0, 0, 0, 0, 0, 0};
int blueColors[30] = {255, 0, 255, 255, 255, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
int directions[30] = {1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1};
int intervals[30] = {100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100};
bool newPeriods[30] = {true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true};
unsigned long periodStarts[30] = {};
int numLEDS[30] = {5, 7, 35, 34, 36, 9, 9, 6, 9, 9, 6, 9, 9, 6, 9, 9, 16, 8, 7, 6, 4, 21, 7, 20, 7, 20};
int firstIndices[30] = {0, 11, 46, 47, 116, 125, 126, 140, 149, 150, 164, 173, 174, 188, 197, 198, 222, 223, 231, 238, 244, 248, 268, 275, 295, 302};
int currentIndices[30] = {0, 11, 46, 47, 116, 125, 126, 140, 149, 150, 164, 173, 174, 188, 197, 198, 222, 223, 231, 238, 244, 248, 268, 275, 295, 302};
int prevIndices[30] = {100, 100, 100, 100, 200, 200, 200, 200, 200, 200, 200, 300, 300, 300, 300, 300, 300, 300, 300, 300, 300, 300, 300, 300, 300, 300};

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
  Serial.begin(115200);
  // Initialize the NeoPixel library.
  pixels.begin();
  for (int i = 0; i < 26; i++) {
    pixels.setPixelColor(firstPixels[i], pixels.Color(redColors[i], greenColors[i], blueColors[i]));
  }
  // defineInterval();
}

void loop() {
  // put your main code here, to run repeatedly:
  currentTime = millis();
  for (int i = 0; i < 26; i++) {
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
