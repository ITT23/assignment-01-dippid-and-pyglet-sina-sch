# Assignment 1

## Exercise 1
Create a program called DIPPID-sender.py based on the simple-sender.py code sample. Your program should be able to simulate DIPPID input devices by sending
data to a DIPPID receiver via UDP to localhost. The program should have at least
the two capabilities accelerometer and button_1.
Implement plausible behavior for the simulated sensors. For example, you
could use sine functions with different frequencies for each axis of the accelerometer and randomly press and release the button.

### **Solution**
Required Packages: socket, time, numpy, random
> Install with `pip install requirements.txt`

The script DIPPID-sender.py is based on the simple-sender.py.
The method `random_button` randomly pressed and released a button.
The method `random_acc` implements an acceleration with sine-functions for each axis.
Run `python3 DIPPID-sender.py` to send this data to port 5701.

## Exercise 2
Implement a simple 2D game (for example Breakout, Space Invaders, Snake, Tetris, …) with Python and pyglet. The game should use DIPPID as an input device.
Use plausible interaction techniques to control your game, for example moving
the player by tilting the device.

### **Solution**
Required packages: pyglet, DIPPID, numpy, sys
> Install with `pip install requirements.txt`

This implementation of breakout is based on the description of rules in https://en.wikipedia.org/wiki/Breakout_(video_game)#Gameplay. 
The class Bricks implements four rows of bricks, each one with a different color. The color represents the amount of points a brick earns (red bricks: 7 points, orange bricks: 5, green: 3, yellow: 1).
After 4 or 12 bricks were hit, the speed of the ball increases. If the ball hits the upper wall for the first time, the width of the paddle decreases. If the ball misses the paddle and hits the bottom wall, the ball has hit all of the bricks or the time is up, the game ends.
The position of the paddle is determined by the input of the y-value of the gravity parameter of DIPPID. This means, the phone (or other input device) has to be rotated so that it lies in your hands like a controller. If you rotate your phone vertically to the left, the paddle also moves to the left side of the window.


