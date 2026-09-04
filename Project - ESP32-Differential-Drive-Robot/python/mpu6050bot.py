# Offset Calculation

import time
import serial

arduino = serial.Serial("/dev/ttyACM0", 115200)

# Give arduino ime after opening serial
time.sleep(2)

print("Keep MPU Still ....")

x_values = []
y_values = []

while len(x_values) < 50:
  data = arduino.readline().decode().strip()

  if not data:
     continue
 
  parts = data.split("|")

  if len(parts) != 3:
     continue
  
  x = int(parts[0].split("=")[1])
  y = int(parts[1].split("=")[1])

  x_values.append(x)
  y_values.append(y)

  print(f"Calibration : {len(x_values)} / 50")

x_offset = sum(x_values) / len(x_values)
y_offset = sum(y_values) / len(y_values)

print(f"X offset = {x_offset:.0f}")
print(f"Y offset = {y_offset:.0f}")
print("Control Started.")

# Wifi Communication Section

import urllib.request as ul

url_1 = "http://192.168.4.1/hello"
response = ul.urlopen(url_1)
data = response.read()
print(data.decode())

# MPU6050 Data Serial Communication 

while True:
  data = arduino.readline().decode().strip()


  try:
     parts = data.split("|")
     x = int(parts[0].split("=")[1])
     y = int(parts[1].split("=")[1])
     z = int(parts[2].split("=")[1])

  except (ValueError, IndexError):
     continue

  # Remove Neutral Effect
  x -= x_offset
  y -= y_offset

  # Deadzone
  
  if abs(x) < 1500:
     x = 0

  if abs(y) < 1500:
     y = 0

  # MPU Control [ Gesture --> Direction ]
  if x < 0:
     forward = 1
  elif x > 0:
     forward = -1
  else:
     forward = 0

  if y < 0:
     turn = -1
  elif y > 0:
     turn = 1
  else:
     turn = 0  

  # Deadzone
#   if abs(forward) < 0.15:
#      forward = 0

#   if abs(turn) < 0.15:
#      turn = 0

  # Limit to -1 to +1
#   forward = max(-1, min(1,forward))
#   turn = max(-1, min(1, turn))

  # print(f"forward = {forward:.2f} || turn = {turn:.2f}")

  # Left - Motor Velocity
  l_m_v = forward + turn
  
  # Right - Motor Velocity
  r_m_v = forward - turn

  # Max
  max_vel = max(abs(l_m_v), abs(r_m_v))   
  
  if max_vel > 1:
      l_m_v /= max_vel
      r_m_v /= max_vel

  print(f"Left Motor Speed = {l_m_v}, Right Motor Speed = {r_m_v}")

  # Sending Velocities
  
  url_2 = f"http://192.168.4.1/motor?left={l_m_v}&right={r_m_v}"
  try:
     response = ul.urlopen(url_2, timeout=1)
     data = response.read()
  except Exception as e:
     print("Wi-Fi Error : ", e)
      