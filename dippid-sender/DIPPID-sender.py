import socket
import time
import numpy as np
import random
import json

IP = '127.0.0.1'
PORT = 5700

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

x = 0

# button is randomly pressed and released
def random_button():
    pressed = random.randint(0, 1)
    return pressed

# sine functions for each axis of the accelerometer
def random_acc(x):
    dic = {}
    dic['x'] = np.sin(x)
    dic['y'] = np.sin(2*x)
    dic['z'] = np.sin(3*x)
    return dic

while True:

    acc = random_acc(x)
    pressed = random_button()
    
    message = {}
    message['accelerometer'] = acc
    message['button_1'] = pressed
    print('message', message)

    sock.sendto(json.dumps(message).encode(), (IP, PORT))

    x += 0.1
    time.sleep(1)

