// Considering motor 1 as the left motor
// and
// Considering motor 2 as the right motor

#define motor1_pin1 13
#define motor1_pin2 12
#define motor2_pin1 14
#define motor2_pin2 27

#include <WiFi.h>
#include <WebServer.h>

const char* ssid = "YOUR_WIFI_SSID";
const char* pass = "YOUR_WIFI_PASSWORD";

WebServer server(80);

// Left Motor Forward Rotation Function
void lmf(float l) {
  analogWrite(motor1_pin1, l);
  analogWrite(motor1_pin2, 0);
}

// Left Motor Backward Rotation Function
void lmb(float l) {
  analogWrite(motor1_pin1, 0);
  analogWrite(motor1_pin2, l);
}

// Left Motor Stop Rotation Function
void lms() {
  analogWrite(motor1_pin1, 0);
  analogWrite(motor1_pin2, 0);
}

// Right Motor Forward Rotation Function
void rmf(float r) {
  analogWrite(motor2_pin1, r);
  analogWrite(motor2_pin2, 0);
}

// Right Motor Backward Rotation Function
void rmb(float r) {
  analogWrite(motor2_pin1, 0);
  analogWrite(motor2_pin2, r);
}

// Right Motor Stop Rotation Function
void rms() {
  analogWrite(motor2_pin1, 0);
  analogWrite(motor2_pin2, 0);
}

void move_motor(float left, float right) {
  
  float l,r;
  l = 255 * abs(left);
  r = 255 * abs(right);

  if (left == 0) {lms();}
  else if (left < 0) {lmb(l);}
  else if (left > 0) {lmf(l);}

  if (right == 0) {rms();}
  else if (right < 0) {rmb(r);}
  else if (right > 0) {rmf(r);}

}

void hello() {
  server.send(200, "text/plain", "Hello Guys !!!");
}

void motor() {
  float left = server.arg("left").toFloat();
  float right = server.arg("right").toFloat();

  Serial.print("Left = ");
  Serial.print(left);
  
  Serial.print("Right = ");
  Serial.println(right);

  move_motor(left, right);
   
  server.send(200, "text/plain", "OK");

}

void setup() {

  pinMode(motor1_pin1, OUTPUT);
  pinMode(motor1_pin2, OUTPUT);
  pinMode(motor2_pin1, OUTPUT);
  pinMode(motor2_pin2, OUTPUT);

  Serial.begin(115200);

  WiFi.softAP(ssid, pass);
  
  server.on("/hello", hello);
  server.on("/motor", motor);


  server.begin();

}

void loop() {
  server.handleClient();
}

