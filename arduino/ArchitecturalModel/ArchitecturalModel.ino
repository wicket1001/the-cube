#include <Adafruit_NeoPixel.h>

//  0 GRD; GRID <-> Panel
//  1 BAT; BATTERIE <-> Panel
//  2 PV0; PV -> Panel
//  3 WND; WIND -> Panel
//  4 STH; SolarThermal / Water -> Panel
//  5 ATR; Attic right
//  6 ATL; Attic left
//  7 ATU; UP Attic
//  8 THR; Third right
//  9 THL; Third left
// 10 THU; UP Third
// 11 SER; Second right
// 12 SEL; Second left
// 13 SEU; UP Second
// 14 FIR; First right
// 15 FIL; First left
// 16 HPP; HeatPump <-> Panel
// 17 THB; ThermalBattery <-> Panel
// 18 TWB; ThermalBattery <-> WaterBuffer
// 19 HWB; HeatPump <-> WaterBuffer
// 20 FIU; UP First Radiators <-> WaterBuffer
// 21 RFI; Radiators First
// 22 RSU; UP Second Radiators
// 23 RSE; Radiators Second
// 24 RTU; UP Third Radiators
// 25 RTI; Radiators Third
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
int colors[10];
int color[] = {0xFF0000, 0xFF0000, 0xFF0000, 0xFF0000, 0xFF0000, 0xFF0000, 0xFF0000, 0xFF0000, 0xFF0000, 0xFF0000,
               0xFF0000, 0xFF0000, 0xFF0000, 0xFF0000, 0xFF0000, 0xFF0000, 0xFF0000, 0xFF0000, 0xFF0000, 0xFF0000,
               0xFF0000, 0xFF0000, 0xFF0000, 0xFF0000, 0xFF0000, 0xFF0000};
int h[] = {0, 0, 0, 120 * CONVERTER, 60 * CONVERTER, 180 * CONVERTER, 300 * CONVERTER, 0, 60 * CONVERTER, 120 * CONVERTER};
int s[] = {0, 0, 255, 255, 255, 255, 255, 255, 255, 255};
int v[] = {0, 255, 255, 255, 255, 255, 255, 192, 128, 128};
int strip[] = {2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2}; // Color

int pin = 5;                // input pin Neopixel is attached to
int totalNum = 350;         // number of neopixels in whole strip
unsigned long currentTime;  // running time for program
int redColors[] = {255, 255, 0, 0, 0, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255};
int greenColors[] = {0, 200, 255, 255, 255, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 0, 0, 0, 0, 0, 0, 0, 0};
int blueColors[] = {255, 0, 255, 255, 255, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
int hueColors[] = {300, 47, 180, 180, 180, 47, 47, 47, 47, 47, 47, 47, 47, 47, 47, 47, 47, 47, 0, 0, 0, 0, 0, 0, 0, 0};
int saturationColors[] = {255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255};
int valueColors[] = {255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255};
int directions[] = {1, -1, -1, 1, -1, -1, 1, -1, -1, 1, -1, -1, 1, -1, -1, 1, -1, 1, 1, 1, 1, 1, 1, 1, 1, 1};
int intervals[] = {20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20};
bool newPeriods[] = {true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true};
unsigned long periodStarts[SEGMENTS] = {};
int numLEDS[] = {5, 7, 35, 34, 36, 9, 9, 6, 9, 9, 6, 9, 9, 6, 9, 9, 16, 8, 7, 6, 3, 20, 7, 20, 6, 20};
int firstIndices[] = {0, 11, 46, 47, 116, 125, 126, 140, 149, 150, 164, 173, 174, 188, 197, 198, 222, 223, 231, 238, 244, 247, 267, 274, 294, 300};
int currentIndices[] = {0, 11, 46, 47, 116, 125, 126, 140, 149, 150, 164, 173, 174, 188, 197, 198, 222, 223, 231, 238, 244, 247, 267, 274, 294, 300};
int prevIndices[] = {100, 100, 100, 100, 200, 200, 200, 200, 200, 200, 200, 300, 300, 300, 300, 300, 300, 300, 300, 300, 300, 300, 300, 300, 300, 300};
int on[] = {2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2};

bool showing = false;

Adafruit_NeoPixel pixels = Adafruit_NeoPixel(totalNum, pin, NEO_GRB + NEO_KHZ800);

String temp;
String name;
String percent_str;
String color_str;
String check_str;
float mini;
float maxi;
float value;
float percent;

int forwardBlink_HSV(int start, int N, int prevN, int num, int h, int s, int v) {
    prevN = N - 1;
    if (N == start && currentTime > 0) {
        prevN = start + num - 1;
    }
    LED_move_HSV(prevN, N, h, s, v);
    return start + (N - start + 1) % num;
}

int backwardBlink_HSV(int start, int N, int prevN, int num, int h, int s, int v) {
    prevN = N + 1;
    if (N == start && currentTime > 0) {
        prevN = start - num + 1;
    }
    LED_move_HSV(prevN, N, h, s, v);
    return start - (start - N + 1 + num) % num;
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
    pixels.setPixelColor(start + (N - start - 3 + num) % num, pixels.ColorHSV(0, 0, 0));
    pixels.setPixelColor(start + (N - start - 2 + num) % num, pixels.ColorHSV(h, s, v / 10 * 1));
    pixels.setPixelColor(start + (N - start - 1 + num) % num, pixels.ColorHSV(h, s, v / 10 * 3));
    pixels.setPixelColor(start + (N - start + 0 + num) % num, pixels.ColorHSV(h, s, v / 10 * 5));
    pixels.setPixelColor(start + (N - start + 1 + num) % num, pixels.ColorHSV(h, s, v / 10 * 7));
    pixels.setPixelColor(start + (N - start + 2 + num) % num, pixels.ColorHSV(h, s, v));
    pixels.setPixelColor(start + (N - start + 3 + num) % num, pixels.ColorHSV(0, 0, 0));
    return start + (N - start + 1 + num) % num;
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

int forwardOff(int start, int N, int prevN, int num, int h, int s, int v) {
    pixels.setPixelColor(start - (start - N - 3 + num) % num, pixels.ColorHSV(0, 0, 0));
    pixels.setPixelColor(start - (start - N - 2 + num) % num, pixels.ColorHSV(0, 0, 0));
    pixels.setPixelColor(start - (start - N - 1 + num) % num, pixels.ColorHSV(0, 0, 0));
    pixels.setPixelColor(start - (start - N + 0 + num) % num, pixels.ColorHSV(0, 0, 0));
    pixels.setPixelColor(start - (start - N + 1 + num) % num, pixels.ColorHSV(0, 0, 0));
    pixels.setPixelColor(start - (start - N + 2 + num) % num, pixels.ColorHSV(0, 0, 0));
    pixels.setPixelColor(start - (start - N + 3 + num) % num, pixels.ColorHSV(0, 0, 0));
    return N;
}

int backwardOff(int start, int N, int prevN, int num, int h, int s, int v) {
    pixels.setPixelColor(start - (start - N - 3 + num) % num, pixels.ColorHSV(0, 0, 0));
    pixels.setPixelColor(start - (start - N - 2 + num) % num, pixels.ColorHSV(0, 0, 0));
    pixels.setPixelColor(start - (start - N - 1 + num) % num, pixels.ColorHSV(0, 0, 0));
    pixels.setPixelColor(start - (start - N + 0 + num) % num, pixels.ColorHSV(0, 0, 0));
    pixels.setPixelColor(start - (start - N + 1 + num) % num, pixels.ColorHSV(0, 0, 0));
    pixels.setPixelColor(start - (start - N + 2 + num) % num, pixels.ColorHSV(0, 0, 0));
    pixels.setPixelColor(start - (start - N + 3 + num) % num, pixels.ColorHSV(0, 0, 0));
    return N;
}

void LED_move_HSV(int prevN, int N, int h, int s, int v) {
    pixels.setPixelColor(N, pixels.ColorHSV(h, s, v));
    pixels.setPixelColor(prevN, pixels.ColorHSV(0, 0, 0));
    //pixels.show();
}

void setup() {
    // put your setup code here, to run once:
    Serial.begin(9600);
    Serial.setTimeout(1);
    // Initialize the NeoPixel library.
    pixels.begin();
    for (int i = 0; i < SEGMENTS; i++) {
        pixels.setPixelColor(firstIndices[i], 0xFF0000);
    }
    // defineInterval();
    for (int i = 0; i < SEGMENTS; i++) {
        intervals[i] = 1000;
        hueColors[i] *= 182;
    }
    colors[0] = BLACK;
    colors[1] = WHITE;
    colors[2] = RED;
    colors[3] = LIME;
    colors[4] = YELLOW;
    colors[5] = CYAN;
    colors[6] = MAGENTA;
    colors[7] = MAROON;
    colors[8] = OLIVE;
    colors[9] = GREEN;
    Serial.println("Ready");
}

float mapper(float x, float in_min, float in_max, float out_min, float out_max) {
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}



char endMarker = '\n';
#define MIN_SPEED 0.02

const byte numChars = 16;
char receivedChars[numChars];   // an array to store the received data

boolean newData = false;
static byte ndx = 0;

void loop() {
    char rc;
    if (Serial.available() > 0 && newData == false) {
        rc = Serial.read();
        if (rc != endMarker) {
            receivedChars[ndx] = rc;
            ndx ++;
            if (ndx >= numChars) {
                ndx = numChars - 1;
            }
        } else {
            receivedChars[ndx] = '\0';
            ndx = 0;
            newData = true;
        }
    }
    if (newData) {
        String data = String(receivedChars);
        //Serial.println(data);
        name = data.substring(0, 2); // 2
        color_str = data.substring(3, 5); // 2
        percent_str = data.substring(6, 12); // 6
        check_str = data.substring(13, 14); // 1

        if (check_str.equals("x")) {

            int index = name.toInt();
            percent = percent_str.toFloat();
            int color_index = color_str.toInt();

            on[index] = 2;
            if (percent == 1) {
                // TODO current index off
                on[index] = 0;
                percent = 1;
            }
            else if (percent > 0) {
                if (percent < MIN_SPEED) {
                    percent = MIN_SPEED;
                }
                //directions[index] = 1;
            } else if (percent < 0) {
                if (percent > -MIN_SPEED) {
                    percent = -MIN_SPEED;
                }
                //directions[index] = -1;
            } else { // if (percent == 0) {
                // TODO current index off
                // period auf infinity
                percent = 10;
            }

            intervals[index] = percent * 1000.0;

            if (index == 15) {
                if (percent > 0.15) {
                    on[index] = 0;
                    intervals[index] = percent * 2000.0;
                }
            }

            Serial.println("Putting |" + String(index) + "| speeding |" + percent_str + "| to (" + String(percent) + ") |" + String(color_index) + "|" + intervals[index]);

            strip[index] = color_index;
        } else {
            // the serial connection mangled
            // TODO maybe set every timer up
        }

        newData = false;
    }
    currentTime = millis();
    showing = false;
    for (int i = 0; i < SEGMENTS; i++) {
        if (newPeriods[i] == true) {
            periodStarts[i] = currentTime;
            newPeriods[i] = false;
            showing = true;
        }
        if (currentTime - periodStarts[i] > intervals[i]) {
            /*
            if (i == 2) { // PV
                if (currentIndices[i] == firstIndices[i]) {
                    directions[i] = -1;
                }
                if (currentIndices[i] == firstIndices[i] - numLEDS[i] + 1) {
                    directions[i] = 1;
                }
            }*/
            if (directions[i] == -1) {
                if (on[i] > 0) {
                    if (numLEDS[i] >= 6) {
                        /*if (on[i] == 2) {
                            currentIndices[i] = backwardStrip(firstIndices[i], currentIndices[i], prevIndices[i], numLEDS[i], hueColors[i], saturationColors[i], valueColors[i]);
                        } else {
                            backwardOff(firstIndices[i], currentIndices[i], prevIndices[i], numLEDS[i], h[strip[i]], s[strip[i]], v[strip[i]]);
                            */
                            currentIndices[i] = backwardBlink_HSV(firstIndices[i], currentIndices[i], prevIndices[i], numLEDS[i], h[strip[i]], s[strip[i]], v[strip[i]]);
                        /*}*/
                    } else {
                        currentIndices[i] = backwardBlink_HSV(firstIndices[i], currentIndices[i], prevIndices[i], numLEDS[i], h[strip[i]], s[strip[i]], v[strip[i]]);
                    }
                } else {
                    backwardOff(firstIndices[i], currentIndices[i], prevIndices[i], numLEDS[i], h[strip[i]], s[strip[i]], v[strip[i]]);
                }
            } else {
                if (on[i] > 0) {
                    if (numLEDS[i] >= 6) {
                        /*if (on[i] == 2) {
                            currentIndices[i] = forwardStrip(firstIndices[i], currentIndices[i], prevIndices[i], numLEDS[i], hueColors[i], saturationColors[i], valueColors[i]);
                        } else {
                            forwardOff(firstIndices[i], currentIndices[i], prevIndices[i], numLEDS[i], h[strip[i]], s[strip[i]], v[strip[i]]);
                            */
                            currentIndices[i] = forwardBlink_HSV(firstIndices[i], currentIndices[i], prevIndices[i], numLEDS[i], h[strip[i]], s[strip[i]], v[strip[i]]);
                        /*}*/
                    } else {
                        currentIndices[i] = forwardBlink_HSV(firstIndices[i], currentIndices[i], prevIndices[i], numLEDS[i], h[strip[i]], s[strip[i]], v[strip[i]]);
                    }
                } else {
                    forwardOff(firstIndices[i], currentIndices[i], prevIndices[i], numLEDS[i], h[strip[i]], s[strip[i]], v[strip[i]]);
                }
            }
            newPeriods[i] = true;
        }
    }
    if (showing) {
        pixels.show();
    }
}
