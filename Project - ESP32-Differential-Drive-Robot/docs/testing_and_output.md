# Testing and Output

This document records the testing stages, observed outputs, and final demonstration results for Project 1: a 2-wheel differential-drive robot controlled via ESP32.

## Testing Overview

The system was tested in stages rather than as a complete robot from the start. Each subsystem was verified individually before integrating into the full control pipeline.

## MPU6050 and I2C Test

An I2C scanner sketch was run on the Arduino Uno to verify communication with the MPU6050 module.

**Result:**
- MPU6050 was detected at I2C address `0x68`
- This confirmed that the Arduino could successfully communicate with the MPU6050 over I2C

## Serial Communication Test

The Arduino firmware was tested for reading and transmitting accelerometer data.

**Setup:**
- Arduino reads accelerometer X, Y, and Z values from the MPU6050
- Data is sent to the laptop via USB serial at 115200 baud

**Observed serial output format:**

```text
X = <value> | Y = <value> | Z = <value>

Example:

X = -1234 | Y = 567 | Z = 16234

## ESP32 Wi-Fi Test

The ESP32 firmware was tested for Wi-Fi and HTTP communication.

Setup:

ESP32 creates a SoftAP with SSID ESP32_CAR
Laptop connects to the ESP32 network
Python programs send HTTP requests to 192.168.4.1
The /hello endpoint was tested first.

Result:

The ESP32 responded with:
Hello Guys !!!
This confirmed basic Wi-Fi/HTTP communication between the laptop and ESP32.
Motor Control Test
Motor commands were sent from the laptop to the ESP32 using the /motor HTTP endpoint.

Testing approach:

Individual motor commands (left and right) were sent separately
Commands used normalized values in the range -1 to +1
The ESP32 converted these into PWM signals for the L298N

Result:

Motor commands were successfully processed by the ESP32
Motors could spin when the wheels were off the ground
The differential-drive command path from laptop → Wi-Fi → ESP32 → L298N → motors was verified

Gamepad Control Test

The gamepad control path was tested using the pygame-based Python program.
Testing approach:
Gamepad axes were read (Axis 0 for turn, Axis 1 for forward/backward)
Inputs were converted into differential-drive commands:
Left  = Forward + Turn
Right = Forward - Turn
Commands were transmitted over Wi-Fi to the ESP32

Result:

Gamepad input was successfully read and converted
Wi-Fi transmission to the ESP32 worked reliably
The gamepad control path was demonstrated successfully
MPU6050 Gesture-Control Test
The gesture-control path was tested using the MPU6050-based Python program.

Testing approach:

MPU6050 was kept still during startup calibration
The Python program collected 50 samples of X and Y values
X and Y offsets were calculated and subtracted from subsequent readings
A deadzone of 1500 raw units was applied after offset removal
Gestures were mapped to directions:
X negative → Forward
X positive → Backward
Y negative → Left
Y positive → Right
Direction commands were converted into differential-drive motor velocities and sent over Wi-Fi to the ESP32

Result:

Calibration successfully removed stationary offsets
Gesture detection produced consistent forward/backward/left/right commands
Wi-Fi transmission to the ESP32 worked reliably
The gesture-control path was demonstrated successfully

Final Demonstration

Both control methods were demonstrated as functional input paths to the robot:

Gamepad control demonstration
MPU6050 gesture-control demonstration

The demonstrations showed that:

The ESP32 could receive motor commands over Wi-Fi from either source
Differential-drive calculations produced correct left/right motor velocities
The software/control pipeline from input → Python → Wi-Fi → ESP32 → L298N → motors was functional

Reference media:

System architecture: [`media/diagrams/system_architecture.png`](../media/diagrams/system_architecture.png)
Prototype photos: [`media/photos/`](../media/photos/)
Hardware Limitation
The L298N motor driver was a limitation during final physical testing.

Observed behavior:

Motors could spin when the wheels were off the ground
Reliable simultaneous operation of both motors under floor-driving load was not achieved consistently
This is a hardware/motor-driver limitation, not a software failure. The control logic and communication pipeline were demonstrated correctly, but the final mechanical driving performance was constrained by the motor-driver stage.
A more efficient modern motor driver is planned as a future hardware improvement.

Project Status
This project is a functional proof-of-concept prototype that successfully demonstrated:

ESP32-based wireless robot control
Wi-Fi communication between laptop and ESP32
Differential-drive command generation
Gamepad-based manual control
MPU6050 accelerometer-based gesture direction control
The software and control architecture for both input methods was validated. However, the final physical driving performance was limited by the L298N motor driver under load.

The project serves as a learning platform for embedded control, wireless communication, and differential-drive robotics, with clear hardware improvements identified for future iterations.
```