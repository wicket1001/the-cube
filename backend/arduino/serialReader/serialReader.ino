String temp;
String data;
String name;
String mini_str;
String maxi_str;
String value_str;
float mini;
float maxi;
float value;
float percent;

void setup() {
  Serial.begin(9600);
  Serial.setTimeout(1);
  Serial.println("Ready");
}

float mapper(float x, float in_min, float in_max, float out_min, float out_max) {
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}

void  loop() {
  while (!Serial.available());
  temp = Serial.readString();
  if (temp.indexOf("\n") == -1) {
    data += temp;
  } else {
    data += temp;
    data = data.substring(0, data.length() - 1);
    // Serial.println(data);

    name = data.substring(0, data.indexOf(";"));
    data = data.substring(data.indexOf(";") + 1, data.length());

    value_str = data.substring(0, data.indexOf(";"));
    data = data.substring(data.indexOf(";") + 1, data.length());

    mini_str = data.substring(0, data.indexOf(";"));
    data = data.substring(data.indexOf(";") + 1, data.length());

    maxi_str = data.substring(0, data.indexOf(";"));
    data = data.substring(data.indexOf(";") + 1, data.length());

    value = value_str.toFloat();
    mini = mini_str.toFloat();
    maxi = maxi_str.toFloat();

    percent = mapper(value, mini, maxi, 0.0, 1.0);

    Serial.println("Putting " + name + " speeding " + percent + " on " + value + " from " + mini + " to " + maxi);
    
    data = "";    
  }
}
