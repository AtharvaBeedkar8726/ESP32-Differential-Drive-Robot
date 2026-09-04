# Software and Control

This document describes the software architecture, control logic, and communication flow for Project 1: a 2-wheel differential-drive robot controlled via ESP32.

## Software Overview

The project consists of four main software components:

| Component | File | Role |
|-----------|------|------|
| ESP32 firmware | `esp32/robot_car_receiver.ino` | Wi-Fi access point, HTTP server, motor control |
| Arduino firmware | `arduino/Arduino_MPU6050_Interface.ino` | MPU6050 I2C interface, serial output |
| Gamepad control | `python/gamepad_bot.py` | Gamepad input → Wi-Fi motor commands |
| Gesture control | `python/mpu6050bot.py` | MPU6050 serial input → Wi-Fi motor commands |

## Control Architecture

The system has two independent control paths that converge at the ESP32:

### Gamepad Control Path

Gamepad → gamepad_bot.py → Wi-Fi → ESP32 HTTP server → Motor control → L298N → Motors

### MPU6050 Gesture Control Path

MPU6050 → Arduino Uno → USB Serial → mpu6050bot.py → Wi-Fi → ESP32 HTTP server → Motor control → L298N → Motors


Both paths produce the same type of command: normalized left and right motor velocities. The ESP32 does not need to know which input method generated the command.

## ESP32 Robot Controller

The ESP32 firmware implements:

- **Wi-Fi SoftAP**: Creates an access point for laptop connection
  - SSID: `ESP32_CAR`
  - Password: `12345678`
  - IP address: `192.168.4.1`

- **HTTP Server** (port 80): Handles two endpoints
  - `/hello` — Test communication
  - `/motor?left=<value>&right=<value>` — Motor control

- **Motor GPIO Mapping**:
  - GPIO 13, 12 → Left motor (control 1, control 2)
  - GPIO 14, 27 → Right motor (control 1, control 2)

- **Motor Command Interpretation**:
  - Positive value → Forward
  - Negative value → Backward
  - Zero → Stop

The ESP32 converts normalized motor values (range -1 to +1) into PWM signals:

```cpp
l = 255 * abs(left);
r = 255 * abs(right);
```

The main loop continuously handles incoming HTTP requests via `server.handleClient()`.

## Gamepad Control

The `gamepad_bot.py` program:

- Initializes the first connected joystick (`Joystick(0)`)
- Reads two axes:
  - **Axis 0** → Steering / turn (left-right)
  - **Axis 1** → Forward / backward

### Control Mapping

```python
forward = -y  # Invert Y axis
turn = x
```

A deadzone of 0.1 is applied to filter small movements:

```python
if abs(forward) < 0.1 → forward = 0
if abs(turn) < 0.1 → turn = 0
```

Pressing button B (button 1) exits the control loop.

## MPU6050 Gesture Control

The `mpu6050bot.py` program:

- Opens serial connection to Arduino at 115200 baud (`/dev/ttyACM0`)
- Waits 2 seconds for serial stabilization

### Calibration

Before gesture detection begins, the program collects 50 samples while the MPU6050 is stationary:

```python
x_offset = average of 50 X samples
y_offset = average of 50 Y samples
```

These offsets are subtracted from all subsequent readings.

### Deadzone

After offset removal, values within ±1500 are treated as zero:

```python
if abs(x) < 1500 → x = 0
if abs(y) < 1500 → y = 0
```

### Gesture → Direction Mapping

For the physical orientation used in this project:

| Accelerometer Axis | Direction |
|--------------------|-----------|
| X negative | Forward |
| X positive | Backward |
| Y negative | Left |
| Y positive | Right |

The program converts detected gestures into discrete direction commands:

- `forward = 1 / -1 / 0`
- `turn = -1 / 1 / 0`

## Differential-Drive Control

Both control programs use the same differential-drive equations to compute motor velocities:

Left = Forward + Turn
Right = Forward - Turn


### Behavior

| Motion | Left Motor | Right Motor |
|--------|------------|-------------|
| Forward only | +1 | +1 |
| Backward only | -1 | -1 |
| Turn left | Slower or reverse | Faster forward |
| Turn right | Faster forward | Slower or reverse |

### Normalization

The computed motor values can temporarily exceed the -1 to +1 range. Both programs normalize them:

```python
max_vel = max(abs(left_motor), abs(right_motor))
if max_vel > 1:
    left_motor  = left_motor / max_vel
    right_motor = right_motor / max_vel
```

This ensures the ESP32 always receives valid normalized commands.

## Communication Flow

### Initial Handshake

Both Python programs first verify Wi-Fi communication:

GET http://192.168.4.1/hello

### Motor Commands

Motor velocities are sent as HTTP GET requests:

GET http://192.168.4.1/motor?left=<value>&right=<value>


The gesture-control program uses a 1-second timeout and catches communication exceptions to handle disconnections gracefully.

### Timing

- Gamepad control loop: ~10 ms between iterations
- Gesture control loop: Continuous serial reading and HTTP updates

## Control Summary

| Feature | Gamepad Control | Gesture Control |
|---------|-----------------|-----------------|
| Input device | Gamepad (joystick) | MPU6050 accelerometer |
| Input processing | `gamepad_bot.py` | `mpu6050bot.py` |
| Communication to ESP32 | Wi-Fi HTTP | Wi-Fi HTTP |
| Control type | Continuous analog | Discrete direction gestures |
| Calibration | None | 50-sample offset calibration |
| Deadzone | 0.1 (axis range) | ±1500 (accelerometer units) |

Both methods produce normalized left/right motor velocities that the ESP32 converts into PWM signals for the L298N motor driver. The architecture keeps the two input paths independent while using a common motor-control interface.