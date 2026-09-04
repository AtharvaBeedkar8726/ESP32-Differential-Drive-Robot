# Wifi Communication Section

import urllib.request as ul

url_1 = "http://192.168.4.1/hello"
response = ul.urlopen(url_1)
data = response.read()
print(data.decode())

# Gamepad Section

import pygame as pg

pg.init()

gamepad = pg.joystick.Joystick(0)

gamepad.init()

while True:

    pg.event.pump()
    x = round(gamepad.get_axis(0), 3)
    y = round(gamepad.get_axis(1), 3)

    forward = -y
    turn = x
    button_B = gamepad.get_button(1)

    if abs(forward) < 0.1:
        forward = 0

    if abs(turn) < 0.1:
        turn = 0

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

    if(button_B) :
        break

    # Sending Velocities


    url_2 = f"http://192.168.4.1/motor?left={l_m_v}&right={r_m_v}"
    response = ul.urlopen(url_2)
    data = response.read()
    
    pg.time.wait(10);

