#include <Adafruit_NeoPixel.h>

int pin = 2;                // input pin Neopixel is attached to
int totalNum = 30;          // number of neopixels in whole strip
unsigned long currentTime;  // running time for program
int firstPixels[3] = {8, 11, 20};
int redColors[3] = {0, 255, 255};
int greenColors[3] = {255, 0, 0};
int blueColors[3] = {0, 255, 0};


// define turbine portion
int turbNum = 8;           // number of neopixels in turbine portion
int turbFirst = 8;         // index of first pixel in portion
int turbPrev = 100;        // initialize previous position
int turbCurr = turbFirst;  // initialize variable to track current index
int turbInterval = 300;    // set interval/speed
bool turbNewPeriod = true;
unsigned long turbPeriodStart;


// define PV portion
int pvNum = 6;         // number of neopixels in turbine portion
int pvFirst = 11;      // index of first pixel in portion
int pvPrev = 100;      // initialize previous position
int pvCurr = pvFirst;  // initialize variable to track current index
int pvInterval = 50;  // set interval/speed
bool pvNewPeriod = true;
unsigned long pvPeriodStart;

// define solar thermal portion
int solarNum = 5;            // number of neopixels in turbine portion
int solarFirst = 20;         // index of first pixel in portion
int solarPrev = 100;         // initialize previous position
int solarCurr = solarFirst;  // initialize variable to track current index
int solarInterval = 100;     // set interval/speed
bool solarNewPeriod = true;
unsigned long solarPeriodStart;

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
  pixels.show();
}

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  // Initialize the NeoPixel library.
  pixels.begin();
	for (byte i = 0; i < 3; i++) {
  pixels.setPixelColor(firstPixels[i], pixels.Color(redColors[i], greenColors[i], blueColors[i]));
}
}


void loop() {
  // put your main code here, to run repeatedly:
  currentTime = millis();
  if (turbNewPeriod == true) {
    turbPeriodStart = currentTime;
    turbNewPeriod = false;
  }
  if (currentTime - turbPeriodStart > turbInterval) {
    turbCurr = backwardBlink(turbFirst, turbCurr, turbPrev, turbNum, redColors[0], greenColors[0], blueColors[0]);
    turbNewPeriod = true;
  }
  if (pvNewPeriod == true) {
    pvPeriodStart = currentTime;
    pvNewPeriod = false;
  }
  if (currentTime - pvPeriodStart > pvInterval) {
    pvCurr = forwardBlink(pvFirst, pvCurr, pvPrev, pvNum, redColors[1], greenColors[1], blueColors[1]);
    pvNewPeriod = true;
  }
  if (solarNewPeriod == true) {
    solarPeriodStart = currentTime;
    solarNewPeriod = false;
  }
  if (currentTime - solarPeriodStart > solarInterval) {
    solarCurr = forwardBlink(solarFirst, solarCurr, solarPrev, solarNum, redColors[2], greenColors[2], blueColors[2]);
    solarNewPeriod = true;
  }
}