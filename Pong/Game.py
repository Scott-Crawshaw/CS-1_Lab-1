# Scott Crawshaw
# game.py
# 1/21/19
# CS1
# This is my submission for lab 1 checkpoint 1

from random import choice

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
    if (left_paddle[1] < PADDLE_SPEED and left_speed < 0) or \
            (left_paddle[1] >= (WINDOW_HEIGHT - PADDLE_HEIGHT) and left_speed > 0):
        left_speed = 0

    # set speed to zero if right paddle is at bottom wall and going down or at top wall and going up
    if (right_paddle[1] < PADDLE_SPEED and right_speed < 0) or \
            (right_paddle[1] >= (WINDOW_HEIGHT - PADDLE_HEIGHT) and right_speed > 0):
        right_speed = 0

    # advance paddles
    right_paddle[1] += right_speed
    left_paddle[1] += left_speed
    ball[0] += ball_x_speed
    ball[1] += ball_y_speed

    check_ball_collision()

    set_fill_color(1, 0, 0)  # red
    draw_rectangle(left_paddle[0], left_paddle[1], PADDLE_WIDTH, PADDLE_HEIGHT)

    set_fill_color(0, 0, 1)  # blue
    draw_rectangle(right_paddle[0], right_paddle[1], PADDLE_WIDTH, PADDLE_HEIGHT)

    set_fill_color(0, 1, 0)  # green
    draw_circle(ball[0], ball[1], BALL_RADIUS)


def reset_ball():
    # start ball with random direction, but ensure the speed remains constant
    global ball_x_speed, ball_y_speed, ball
    ball_x_speed = choice([-BALL_SPEED, BALL_SPEED])
    ball_y_speed = choice([-BALL_SPEED, BALL_SPEED])
    ball = [WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2]


def check_ball_collision():
    global ball_y_speed, ball_x_speed, left_score, right_score
    if ball[1] - BALL_RADIUS <= 0 and ball_y_speed < 0:  # check ceiling collision
        ball_y_speed = -ball_y_speed
    if ball[1] + BALL_RADIUS >= WINDOW_HEIGHT and ball_y_speed > 0:  # check floor collision
        ball_y_speed = -ball_y_speed
    if ball[0] - BALL_RADIUS <= PADDLE_WIDTH and ball[0] >= PADDLE_WIDTH and ball_x_speed < 0 and ball[1] >= \
            left_paddle[1] and ball[1] <= left_paddle[1] + PADDLE_HEIGHT:
        ball_x_speed = -ball_x_speed
    elif ball[0] - BALL_RADIUS <= 0:
        right_score += 1
        reset_ball()
    if ball[0] + BALL_RADIUS >= WINDOW_WIDTH - PADDLE_WIDTH and ball[
        0] <= WINDOW_WIDTH - PADDLE_WIDTH and ball_x_speed > 0 and ball[1] >= right_paddle[1] and ball[1] <= \
            right_paddle[1] + PADDLE_HEIGHT:
        ball_x_speed = -ball_x_speed
    elif ball[0] + BALL_RADIUS >= WINDOW_WIDTH:
        left_score += 1
        reset_ball()


PADDLE_WIDTH = 10
PADDLE_HEIGHT = 90

WINDOW_HEIGHT = 600
WINDOW_WIDTH = 800

# start paddles in middle of their respective goals
left_paddle = [0, (WINDOW_HEIGHT / 2) - (PADDLE_HEIGHT / 2)]  # x and y coords
right_paddle = [WINDOW_WIDTH - PADDLE_WIDTH, (WINDOW_HEIGHT / 2) - (PADDLE_HEIGHT / 2)]  # x and y coords

LEFT_PADDLE_UP = 'a'
LEFT_PADDLE_DOWN = 'z'
RIGHT_PADDLE_UP = 'k'
RIGHT_PADDLE_DOWN = 'm'

PADDLE_SPEED = 5
BALL_SPEED = 3
BALL_RADIUS = 10

left_score = 0
right_score = 0

left_speed = 0
right_speed = 0

reset_ball()

start_graphics(draw_table, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, key_press=key_pressed)
