import socket
import time
import numpy as np
import random

IP = '127.0.0.1'
PORT = 5701

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

x = 0

# button is randomly pressed and released
def random_button():
    pressed = random.randint(0, 1)
    return pressed

# sine functions for each axis of the accelerometer
def random_acc(x):
    dict = {}
    dict['x'] = np.sin(x)
    dict['y'] = np.sin(2*x)
    dict['z'] = np.sin(3*x)
    return dict

while True:

    acc = random_acc(x)
    pressed = random_button()
    
    message = {}
    message['acceleration'] = acc
    message['button'] = pressed
    print('message', message)

    sock.sendto(str(message).encode(), (IP, PORT))

    x += 0.1
    time.sleep(1)

