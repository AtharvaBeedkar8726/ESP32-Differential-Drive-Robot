# Hardware and Wiring

This document describes the hardware components, wiring, and physical prototype for Project 1: a 2-wheel differential-drive robot controlled via ESP32.

## Hardware

The main components used in this prototype are:

- ESP32 development board (main controller for motor control and Wi-Fi)
- L298N motor driver
- 2 × small DC geared motors
- 2 × wheels
- Simple prototype chassis/frame
- Arduino Uno (used only for MPU6050 gesture-control path)
- MPU6050 / GY-521 module (accelerometer/gyroscope for gesture control)
- Gamepad (for manual control)
- Laptop (runs Python programs for both control methods)
- Battery/power source
- Connecting wires

## ESP32 → L298N

The ESP32 directly controls the L298N motor driver using the following GPIO pins:

| ESP32 GPIO | L298N Connection | Motor Function        |
|------------|------------------|-----------------------|
| GPIO 13    | Left control 1   | Left motor control 1  |
| GPIO 12    | Left control 2   | Left motor control 2  |
| GPIO 14    | Right control 1  | Right motor control 1 |
| GPIO 27    | Right control 2  | Right motor control 2 |

The L298N then drives the two DC motors. Motor 1 is the left motor, and Motor 2 is the right motor.

## Arduino Uno → MPU6050

The MPU6050 is connected to the Arduino Uno via I2C for gesture-based control:

| Arduino Uno | MPU6050 |
|-------------|---------|
| 3.3V        | VCC     |
| GND         | GND     |
| A4          | SDA     |
| A5          | SCL     |

The MPU6050 I2C address is `0x68`. The Arduino reads accelerometer data and sends it over USB serial to the laptop.

## Control Connections

This project supports two independent control methods that both send commands to the same ESP32:

### Gamepad Control

Gamepad → Laptop (Python) → Wi-Fi → ESP32 → L298N → Motors

### MPU6050 Gesture Control

MPU6050 → Arduino Uno → USB Serial → Laptop (Python) → Wi-Fi → ESP32 → L298N → Motors


The ESP32 creates a Wi-Fi access point with the following settings:

- **SSID:** `ESP32_CAR`
- **Password:** `12345678`
- **IP address:** `192.168.4.1`

The laptop connects to this network, and the Python programs send HTTP requests to the ESP32 for motor control.

## Prototype

The robot is assembled as a functional prototype using a simple chassis/frame with a basic motor mounting arrangement. It is designed for testing and learning, not as a polished mechanical design.

Reference photos of the prototype are available in the `media/photos/` directory:

- [`RC_CAR_Prototype_Front_View.jpg`](../media/photos/RC_CAR_Prototype_Front_View.jpg)
- [`RC_CAR_Prototype_Back_View.jpg`](../media/photos/RC_CAR_Prototype_Back_View.jpg)
- [`RC_CAR_Prototype_Top_View.jpg`](../media/photos/RC_CAR_Prototype_Top_View.jpg)
- [`RC_CAR_Prototype_Orthogonal_View.jpg`](../media/photos/RC_CAR_Prototype_Orthogonal_View.jpg)
- [`RC_CAR_Prototype_Motor_Mounting.jpg`](../media/photos/RC_CAR_Prototype_Motor_Mounting.jpg)

## Hardware Limitation

During testing, the L298N motor driver showed limitations under load. The motors could spin reliably with the wheels off the ground, but consistent simultaneous operation of both motors under floor-driving load was not achieved.

This is a hardware/motor-driver limitation, not a software issue. A more efficient modern motor driver is planned as a future improvement.