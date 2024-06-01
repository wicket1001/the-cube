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

// Net Overproduction Electricity Lime
// Battery Supply Green
// Net Grid Yellow

// Grid Purple

// Radiators SandBattery, HeatPump Olive
// Radiators Grid Maroon

#define SEGMENTS 26

#define CONVERTER 182

#define   BLACK pixels.ColorHSV(0, 0, 0)
#define   WHITE pixels.ColorHSV(0, 0, 255)
#define     RED pixels.ColorHSV(0, 255, 255)
#define    LIME pixels.ColorHSV(120 * CONVERTER, 255, 255)
#define  YELLOW pixels.ColorHSV(60 * CONVERTER, 255, 255)
#define    CYAN pixels.ColorHSV(180 * CONVERTER, 255, 255)
#define MAGENTA pixels.ColorHSV(300 * CONVERTER, 255, 255)
#define  MAROON pixels.ColorHSV(0, 255, 192)
#define   OLIVE pixels.ColorHSV(60 * CONVERTER, 255, 128)
#define   GREEN pixels.ColorHSV(120 * CONVERTER, 255, 128)

int pin = 5;                // input pin Neopixel is attached to
int totalNum = 350;         // number of neopixels in whole strip
unsigned long currentTime;  // running time for program
int redColors[SEGMENTS] = {255, 255, 0, 0, 0, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255};
int greenColors[SEGMENTS] = {0, 200, 255, 255, 255, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 0, 0, 0, 0, 0, 0, 0, 0};
int blueColors[SEGMENTS] = {255, 0, 255, 255, 255, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
int hueColors[SEGMENTS] = {300, 47, 180, 180, 180, 47, 47, 47, 47, 47, 47, 47, 47, 47, 47, 47, 47, 47, 0, 0, 0, 0, 0, 0, 0, 0};
int saturationColors[SEGMENTS] = {255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255};
int valueColors[SEGMENTS] = {255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255};
int directions[SEGMENTS] = {1, -1, -1, 1, -1, -1, 1, -1, -1, 1, -1, -1, 1, -1, -1, 1, -1, 1, 1, 1, 1, 1, 1, 1, 1, 1};
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
    return start + (N + 1) % num;
}

int forwardBlink_HSV(int start, int N, int prevN, int num, int h, int s, int v) {
    prevN = N - 1;
    if (N == start && currentTime > 0) {
        prevN = start + num - 1;
    }
    LED_move_HSV(prevN, N, h, s, v);
    return start + (N + 1) % num;
}

int backwardBlink(int start, int N, int prevN, int num, int red, int green, int blue) {
    prevN = N + 1;
    if (N == start && currentTime > 0) {
        prevN = start - num + 1;
    }
    LED_move(prevN, N, red, green, blue);
    return start - (start - N + 1) % num;
}

int backwardBlink_HSV(int start, int N, int prevN, int num, int h, int s, int v) {
    prevN = N + 1;
    if (N == start && currentTime > 0) {
        prevN = start - num + 1;
    }
    LED_move_HSV(prevN, N, h, s, v);
  N--;
  if (N == start - num) {
    N = start;
  }
  return N;
}

int forwardGaus(int start, int N, int prevN, int num, int h, int s, int v) {
    pixels.setPixelColor((N - 3 + num) % num + start, pixels.ColorHSV(0, 0, 0));
    pixels.setPixelColor((N - 2 + num) % num + start, pixels.ColorHSV(h, s / 4 * 3, v));
    pixels.setPixelColor((N - 1 + num) % num + start, pixels.ColorHSV(h, s / 8 * 7, v));
    pixels.setPixelColor((N + 0 + num) % num + start, pixels.ColorHSV(h, s, v));
    pixels.setPixelColor((N + 1 + num) % num + start, pixels.ColorHSV(h, s / 8 * 7, v));
    pixels.setPixelColor((N + 2 + num) % num + start, pixels.ColorHSV(h, s / 4 * 3, v));
    pixels.setPixelColor((N + 3 + num) % num + start, pixels.ColorHSV(0, 0, 0));
    return start + (N + 1) % num;
}

int forwardStrip(int start, int N, int prevN, int num, int h, int s, int v) {
    pixels.setPixelColor((N - 3 + num) % num + start, pixels.ColorHSV(0, 0, 0));
    pixels.setPixelColor((N - 2 + num) % num + start, pixels.ColorHSV(h, s, v / 10 * 1));
    pixels.setPixelColor((N - 1 + num) % num + start, pixels.ColorHSV(h, s, v / 10 * 3));
    pixels.setPixelColor((N + 0 + num) % num + start, pixels.ColorHSV(h, s, v / 10 * 5));
    pixels.setPixelColor((N + 1 + num) % num + start, pixels.ColorHSV(h, s, v / 10 * 7));
    pixels.setPixelColor((N + 2 + num) % num + start, pixels.ColorHSV(h, s, v));
    pixels.setPixelColor((N + 3 + num) % num + start, pixels.ColorHSV(0, 0, 0));
    return start + (N + 1) % num;
}

int backwardStrip(int start, int N, int prevN, int num, int h, int s, int v) {
    pixels.setPixelColor(start - (start - N - 3 + num) % num, pixels.ColorHSV(0, 0, 0));
    pixels.setPixelColor(start - (start - N - 2 + num) % num, pixels.ColorHSV(h, s, v / 6 * 2));
    pixels.setPixelColor(start - (start - N - 1 + num) % num, pixels.ColorHSV(h, s, v / 6 * 3));
    pixels.setPixelColor(start - (start - N + 0 + num) % num, pixels.ColorHSV(h, s, v / 6 * 4));
    pixels.setPixelColor(start - (start - N + 1 + num) % num, pixels.ColorHSV(h, s, v / 6 * 5));
    pixels.setPixelColor(start - (start - N + 2 + num) % num, pixels.ColorHSV(h, s, v));
    pixels.setPixelColor(start - (start - N + 3 + num) % num, pixels.ColorHSV(0, 0, 0));
    return start - (start - N + 1 + num) % num;
}

void LED_move_HSV(int prevN, int N, int h, int s, int v) {
    pixels.setPixelColor(N, pixels.ColorHSV(h, s, v));
    pixels.setPixelColor(prevN, pixels.ColorHSV(0, 0, 0));
    //pixels.show();
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
    for (int i = 0; i < SEGMENTS; i++) {
        pixels.setPixelColor(firstIndices[i], pixels.ColorHSV(hueColors[i], saturationColors[i], valueColors[i]));
    }
    // defineInterval();
    for (int i = 0; i < SEGMENTS; i++) {
        intervals[i] = 20;
        hueColors[i] *= 182;
    }
}

void loop() {
    // put your main code here, to run repeatedly:
    currentTime = millis();
    for (int i = 12; i < 13; i++) {
        if (newPeriods[i] == true) {
            periodStarts[i] = currentTime;
            newPeriods[i] = false;
        }
        if (currentTime - periodStarts[i] > intervals[i]) {
            if (i == 2) { // PV
                if (currentIndices[i] == firstIndices[i]) {
                    directions[i] = -1;
                }
                if (currentIndices[i] == firstIndices[i] - numLEDS[i] + 1) {
                    directions[i] = 1;
                }
            }
            if (directions[i] >= 6) {
                /*if (numLEDS[i] == -1) {
                    currentIndices[i] = backwardStrip(firstIndices[i], currentIndices[i], prevIndices[i], numLEDS[i], hueColors[i], saturationColors[i], valueColors[i]);
                } else {
                    currentIndices[i] = backwardBlink_HSV(firstIndices[i], currentIndices[i], prevIndices[i], numLEDS[i], hueColors[i], saturationColors[i], valueColors[i]);
                }*/
            } else {
                if (numLEDS[i] == -1) {
                    currentIndices[i] = forwardStrip(firstIndices[i], currentIndices[i], prevIndices[i], numLEDS[i], hueColors[i], saturationColors[i], valueColors[i]);
                } else {
                    currentIndices[i] = forwardBlink_HSV(firstIndices[i], currentIndices[i], prevIndices[i], numLEDS[i], hueColors[i], saturationColors[i], valueColors[i]);
                }
            }
            newPeriods[i] = true;
        }
    }
    pixels.show();
}
