#Scott Crawshaw
# game.py
# 1/21/19
# CS1
# This is my submission for lab 1 checkpoint 1

from cs1lib import *


def key_pressed(key):
    global left_speed, right_speed

    if key is LEFT_PADDLE_UP:
        left_speed = -PADDLE_SPEED
    if key is LEFT_PADDLE_DOWN:
        left_speed = PADDLE_SPEED
    if key is RIGHT_PADDLE_DOWN:
        right_speed = PADDLE_SPEED
    if key is RIGHT_PADDLE_UP:
        right_speed = -PADDLE_SPEED


def draw_table():
    global left_paddle, right_paddle, left_speed, right_speed

    set_clear_color(1, 1, 1)  # set background white
    clear()

    # set speed to zero if left paddle is at bottom wall and going down or at top wall and going up
    if (left_paddle[1] < PADDLE_SPEED and left_speed < 0) or (
            left_paddle[1] >= (WINDOW_HEIGHT - PADDLE_HEIGHT) and left_speed > 0):
        left_speed = 0

    # set speed to zero if right paddle is at bottom wall and going down or at top wall and going up
    if (right_paddle[1] < PADDLE_SPEED and right_speed < 0) or (
            right_paddle[1] >= (WINDOW_HEIGHT - PADDLE_HEIGHT) and right_speed > 0):
        right_speed = 0

    # advance paddles
    right_paddle[1] += right_speed
    left_paddle[1] += left_speed

    set_fill_color(1, 0, 0)  # red
    draw_rectangle(left_paddle[0], left_paddle[1], PADDLE_WIDTH, PADDLE_HEIGHT)

    set_fill_color(0, 0, 1)  # green
    draw_rectangle(right_paddle[0], right_paddle[1], PADDLE_WIDTH, PADDLE_HEIGHT)


PADDLE_WIDTH = 20
PADDLE_HEIGHT = 90

WINDOW_HEIGHT = 600
WINDOW_WIDTH = 800

# start paddles in middle of their respective goals
left_paddle = [0, (WINDOW_HEIGHT / 2) - (PADDLE_HEIGHT / 2)]
right_paddle = [WINDOW_WIDTH - PADDLE_WIDTH, (WINDOW_HEIGHT / 2) - (PADDLE_HEIGHT / 2)]

LEFT_PADDLE_UP = 'a'
LEFT_PADDLE_DOWN = 'z'
RIGHT_PADDLE_UP = 'k'
RIGHT_PADDLE_DOWN = 'm'

PADDLE_SPEED = 5

left_speed = 0
right_speed = 0

start_graphics(draw_table, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, key_press=key_pressed)