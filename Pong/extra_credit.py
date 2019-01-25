# Scott Crawshaw
# extra_credit.py
# 1/25/19
# CS1
# This is my extra credit submission for lab 1

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

    if key is RESET_GAME:
        new_game()
    if key is QUIT_GAME:
        cs1_quit()


def new_game():
    global left_score, right_score, left_speed, right_speed, left_paddle, right_paddle
    left_score = 0
    right_score = 0

    left_speed = 0
    right_speed = 0

    # start paddles in middle of their respective goals
    left_paddle = [0, (WINDOW_HEIGHT / 2) - (PADDLE_HEIGHT / 2)]  # x and y coords
    right_paddle = [WINDOW_WIDTH - PADDLE_WIDTH, (WINDOW_HEIGHT / 2) - (PADDLE_HEIGHT / 2)]  # x and y coords

    reset_ball()


def reset_ball():  # start ball in center of screen
    global ball_x_speed, ball_y_speed, ball

    # randomize ball initial direction
    ball_x_speed = choice([BALL_SPEED, -BALL_SPEED])
    ball_y_speed = choice([BALL_SPEED, -BALL_SPEED])
    ball = [WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2]


def check_ball_collision():  # see if ball has collided with any relevant features
    global ball_y_speed, ball_x_speed, left_score, right_score

    if ball[1] - BALL_RADIUS <= 0 and ball_y_speed < 0:  # check ceiling collision
        ball_y_speed = -ball_y_speed

    if ball[1] + BALL_RADIUS >= WINDOW_HEIGHT and ball_y_speed > 0:  # check floor collision
        ball_y_speed = -ball_y_speed

    if ball[0] - BALL_RADIUS <= PADDLE_WIDTH and ball[0] >= PADDLE_WIDTH and ball_x_speed < 0 and ball[1] >= \
            left_paddle[1] and ball[1] <= left_paddle[1] + PADDLE_HEIGHT:  # check left paddle collision
        ball_x_speed = -ball_x_speed
    elif ball[0] - BALL_RADIUS <= 0:  # check left wall collision
        right_score += 1
        reset_ball()

    if ball[0] + BALL_RADIUS >= WINDOW_WIDTH - PADDLE_WIDTH and ball[
        0] <= WINDOW_WIDTH - PADDLE_WIDTH and ball_x_speed > 0 and ball[1] >= right_paddle[1] and ball[1] <= \
            right_paddle[1] + PADDLE_HEIGHT:  # check right paddle collision
        ball_x_speed = -ball_x_speed
    elif ball[0] + BALL_RADIUS >= WINDOW_WIDTH:  # check right wall collision
        left_score += 1
        reset_ball()


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

    check_ball_collision()

    # advance paddles and ball
    right_paddle[1] += right_speed
    left_paddle[1] += left_speed
    ball[0] += ball_x_speed
    ball[1] += ball_y_speed

    # draw left paddle
    set_fill_color(1, 0, 0)  # red
    draw_rectangle(left_paddle[0], left_paddle[1], PADDLE_WIDTH, PADDLE_HEIGHT)

    # draw right paddle
    set_fill_color(0, 0, 1)  # blue
    draw_rectangle(right_paddle[0], right_paddle[1], PADDLE_WIDTH, PADDLE_HEIGHT)

    # draw ball
    set_fill_color(0, 1, 0)  # green
    draw_circle(ball[0], ball[1], BALL_RADIUS)

    # draw score
    set_stroke_color(0, 0, 0)  # black
    set_font_bold()
    set_font_size(25)
    draw_text(str(left_score), WINDOW_WIDTH / 3, WINDOW_HEIGHT / 5)
    draw_text(str(right_score), (WINDOW_WIDTH * 2) / 3, WINDOW_HEIGHT / 5)


PADDLE_WIDTH = 10
PADDLE_HEIGHT = 90

WINDOW_HEIGHT = 600
WINDOW_WIDTH = 800

LEFT_PADDLE_UP = 'a'
LEFT_PADDLE_DOWN = 'z'
RIGHT_PADDLE_UP = 'k'
RIGHT_PADDLE_DOWN = 'm'
RESET_GAME = ' '
QUIT_GAME = 'q'

PADDLE_SPEED = 5
BALL_SPEED = 4
BALL_RADIUS = 10

left_score = 0
right_score = 0

left_speed = 0
right_speed = 0

# start paddles in middle of their respective goals
left_paddle = [0, (WINDOW_HEIGHT / 2) - (PADDLE_HEIGHT / 2)]  # x and y coords
right_paddle = [WINDOW_WIDTH - PADDLE_WIDTH, (WINDOW_HEIGHT / 2) - (PADDLE_HEIGHT / 2)]  # x and y coords

reset_ball()

start_graphics(draw_table, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, key_press=key_pressed)
