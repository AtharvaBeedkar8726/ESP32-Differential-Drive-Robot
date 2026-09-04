#include<Wire.h>

#define MPU6050_ADDR 0x68

int16_t accelX;
int16_t accelY;
int16_t accelZ;

void setup() {
  Serial.begin(115200);
  Wire.begin();

  // Start MPU6050

  Wire.beginTransmission(MPU6050_ADDR);
  Wire.write(0x6B);
  Wire.write(0);
  Wire.endTransmission();

}

void loop() {

  // Start Reading Acceleration register
  Wire.beginTransmission(MPU6050_ADDR);
  Wire.write(0x3B);
  Wire.endTransmission(false);

  Wire.requestFrom(MPU6050_ADDR, 6);

  accelX = Wire.read() << 8 | Wire.read();
  accelY = Wire.read() << 8 | Wire.read();
  accelZ = Wire.read() << 8 | Wire.read();

  Serial.print(" X = ");
  Serial.print(accelX);

  Serial.print(" | Y = ");
  Serial.print(accelY);
  
  Serial.print(" | Z = ");
  Serial.println(accelZ);
}
