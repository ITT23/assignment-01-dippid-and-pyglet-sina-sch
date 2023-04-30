import pyglet
from pyglet import window, clock, shapes
from DIPPID import SensorUDP
import numpy as np
import sys

# use UPD (via WiFi) for communication
PORT = 5701
sensor = SensorUDP(PORT)

WINDOW_HEIGHT=600
WINDOW_WIDTH=450

window = window.Window(WINDOW_WIDTH, WINDOW_HEIGHT)

batch = pyglet.graphics.Batch()

# display score
score_label = pyglet.text.Label(text='Score: 0',
                                font_name='Arial',
                                font_size=18,
                                x=WINDOW_WIDTH - 120, y= WINDOW_HEIGHT - 30,
                                batch=batch)
score = 0

# display timer
timer_label = pyglet.text.Label(text='01:30',
                                font_name='Arial',
                                font_size=18,
                                x=10, y= WINDOW_HEIGHT - 30,
                                batch=batch)
# timer is at 90s
game_over_time = 90

t = 0

# function from pyglet_click.py
def measure_distance(x1, y1, x2, y2):
    distance = np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
    return distance

# implement bricks
class Brick:

    bricks = []

    def __init__(self, x, y, color, score):
        self.x = x
        self.y = y
        self.width = 25
        self.height = 15
        self.color = color
        self.score = score
        self.shape = shapes.Rectangle(  x=self.x,
                                        y=self.y,
                                        width=self.width,
                                        height=self.height,
                                        color=self.color,
                                        batch=batch)
        
    # 8 rows of bricks, 2 of each color, 14 columns   
    # depending on the color the amount of increasement of the score changes 
    def create_bricks():
        for row in range(4):
            if row < 1:
                # red
                color = (205, 38, 38)
                score = 7
            elif row < 2:
                # orange
                color = (255, 140, 0)
                score = 5
            elif row < 3:
                # green
                color = (154, 205, 50)
                score = 3
            else:
                # yellow
                color = (255, 215, 0)
                score = 1
            # calculate y-coordinate
            y = 500 - (10 * (row + 1) + 15 * row)
            for col in range(14):
                # calculate x-coordinate
                x = 7 * (col + 1) + 25 * col
                Brick.bricks.append(Brick(x, y, color, score))

    # update list of bricks after collision with the ball
    def update_bricks():
        for brick in Brick.bricks:
            if ball.collides_with(brick):
                ball.handle_collision_with(brick)

# implement paddle
class Paddle():
    def __init__(self, x=225):
        self.x = 225
        self.y = 45
        self.width = 55
        self.height = 7
        self.color = (240, 248, 255)
        self.shape = shapes.Rectangle(x=self.x, 
                                      y=self.y, 
                                      width=self.width, 
                                      height=self.height, 
                                      color=self.color,
                                      batch=batch)

    # update paddle position depending on rotation of phone    
    def update_paddle():
        pos_x = paddle.shape.x
        if(sensor.has_capability('gravity')):
            y = float(sensor.get_value('gravity')['y'])
            pos_x = WINDOW_WIDTH / 2 + y * 30
            # check for borders
            if pos_x < 0:
                pos_x = 0
            elif pos_x > WINDOW_WIDTH - paddle.width:
                pos_x = WINDOW_WIDTH - paddle.width
        return pos_x

# implement ball
class Ball():

    def __init__(self, x=240, y=100):
        self.x = x 
        self.y = y
        self.direction_x = 1
        self.direction_y = 1
        self.radius = 10
        self.color = (240, 248, 255)
        self.shape = shapes.Circle( x=self.x, 
                                    y=self.y, 
                                    radius=self.radius,
                                    color=self.color,
                                    batch=batch)

    # check borders of the window to prevent the ball from flying out of the window
    def check_borders(self):
        decrease_paddle = False
        x_min = self.radius
        x_max = WINDOW_WIDTH - self.radius
        y_min = self.radius
        y_max = WINDOW_HEIGHT - self.radius
        if self.shape.x < x_min:
            self.direction_x = 1
        elif self.shape.x > x_max:
            self.direction_x = -1
        if self.shape.y < y_min:
            # if ball touches the bottom of the window -> GAME OVER
            clock.schedule_interval(game_over, 0.005)
        elif self.shape.y > y_max:
            self.direction_y = -1
            # if ball hits upper wall, paddle width decreases
            decrease_paddle = True
        return decrease_paddle

    # determine if the ball collides with a brick or the paddle
    def collides_with(self, other):
        if other in Brick.bricks:
            collision_distance = self.radius + other.height
        else:
            collision_distance = self.radius + other.height * 2
        actual_distance = measure_distance(self.shape.x, self.shape.y, other.shape.x + other.width/2, other.shape.y)
        return (actual_distance <= collision_distance)

    # if the ball collides with another object, change direction of the ball
    # if the other object is a brick, remove the brick
    def handle_collision_with(self, other):
        self.direction_y = self.direction_y * (-1)
        if other in Brick.bricks:
            global score
            Brick.bricks.remove(other)
            score += other.score

def increase_speed(num_bricks):
    update_interval = 0.005
    # increase speed a bit after a certain amount of hits
    hits = num_bricks - len(Brick.bricks)
    if hits >= 4:
        update_interval = 0.004
    if hits >= 12:
        update_interval = 0.003
    return update_interval

@window.event
def update(dt, num_bricks):
    window.clear()
    global t, paddle, ball, score_label

    # update paddle position depending on rotation of phone
    paddle.shape.x = Paddle.update_paddle()
    # update ball position
    ball.shape.x += ball.direction_x
    ball.shape.y += ball.direction_y
    # make sure that ball is in the window
    decrease_paddle = ball.check_borders()
    # decrease paddle width if the ball hits the uppper wall
    if decrease_paddle:
        paddle.shape.width = 35
    t += 1
    # check if the ball collides with any brick
    # if yes, ball changes direction and brick is removed
    Brick.update_bricks()
    # if all bricks are removed, game ends
    if len(Brick.bricks) == 0:
        clock.schedule_interval(game_over, 0.005)
    # increase speed after a certain amount of bricks were hit
    update_interval = increase_speed(num_bricks)
    # update score text
    score_label.text = "Score: " + str(score)
    # check if ball collides with the paddle
    # if yes, change direction of the ball
    if ball.collides_with(paddle):
        ball.handle_collision_with(paddle)

    batch.draw()

@window.event
def game_over_handler(dt):
    clock.schedule_interval(game_over, 0.003)

@window.event
def game_over(dt):
    global score
    if len(Brick.bricks) != 0:
        game_over_label = pyglet.text.Label(text='GAME OVER',
                                            font_name='Arial',
                                            font_size=36,
                                            x=75, y= WINDOW_HEIGHT /2)
        clock.unschedule(update)
        window.clear()
        game_over_label.draw()
    else:
        congrats_label = pyglet.text.Label(text='Congratulations!',
                                            font_name='Arial',
                                            font_size=26,
                                            x=10, y= WINDOW_HEIGHT /2)
        clock.unschedule(update)
        window.clear()
        congrats_label.draw()
    score_label.text = "Score: " + str(score)
    score_label.draw()

@window.event 
def countdown(dt):
    global game_over_time
    mins, secs = divmod(game_over_time, 60)
    timer = '{:02d}:{:02d}'.format(mins, secs)
    timer_label.text = timer
    game_over_time -= 1

# code from pyglet_click.py
@window.event
def on_key_press(symbol, modifiers):
    if symbol == pyglet.window.key.Q:
        sys.exit(0)


if __name__ == '__main__':
    # create the ball and the paddle
    ball = Ball()
    paddle = Paddle()
    # create all of the bricks
    Brick.create_bricks()
    num_bricks = len(Brick.bricks)
    #clock.schedule_interval(increase_speed, 0.005, num_bricks)
    # update every 0.005 seconds
    update_interval = 0.005
    clock.schedule_interval(update, update_interval, num_bricks)
    clock.schedule_interval(countdown, 1)
    clock.schedule_once(game_over_handler, 90)

    pyglet.app.run()