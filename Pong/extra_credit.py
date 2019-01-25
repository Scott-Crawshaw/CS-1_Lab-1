# Scott Crawshaw
# extra_credit.py
# 1/25/19
# CS1
# This is my extra credit submission for lab 1

from random import choice, randint
from time import time

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

    if key is RIGHT_SHOOT and right_reloaded:
        create_bullet('right')
    if key is LEFT_SHOOT and left_reloaded:
        create_bullet('left')


def new_game():
    global left_score, right_score, left_speed, right_speed, left_paddle, right_paddle
    global left_gun, right_gun, left_bullets, right_bullets, left_reloaded, right_reloaded
    left_score = 0
    right_score = 0

    left_speed = 0
    right_speed = 0

    # start paddles in middle of their respective goals
    left_paddle = [0, (WINDOW_HEIGHT / 2) - (PADDLE_HEIGHT / 2)]  # x and y coords
    right_paddle = [WINDOW_WIDTH - PADDLE_WIDTH, (WINDOW_HEIGHT / 2) - (PADDLE_HEIGHT / 2)]  # x and y coords

    # create guns in middle of paddles
    left_gun = [PADDLE_WIDTH, (WINDOW_HEIGHT / 2) - (GUN_HEIGHT / 2)]
    right_gun = [WINDOW_WIDTH - PADDLE_WIDTH - GUN_WIDTH, (WINDOW_HEIGHT / 2) - (GUN_HEIGHT / 2)]

    left_bullets = []
    right_bullets = []

    left_reloaded = True
    right_reloaded = True

    reset_ball()


def reset_ball():  # start ball in center of screen
    global ball_x_speed, ball_y_speed, ball

    # randomize ball initial direction
    ball_x_speed = choice([BALL_SPEED, -BALL_SPEED])
    ball_y_speed = choice([BALL_SPEED, -BALL_SPEED])
    ball = [WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2]
    change_ball_color()


def change_ball_color():
    global ball_color

    # set ball color randomly, but make sure its never pure white
    ball_color = [randint(0, 90) / 100, randint(0, 90) / 100, randint(0, 90) / 100]


def check_ball_collision():  # see if ball has collided with any relevant features
    global ball_y_speed, ball_x_speed, left_score, right_score

    if ball[1] - BALL_RADIUS <= 0 and ball_y_speed < 0:  # check ceiling collision
        ball_y_speed = -ball_y_speed

    if ball[1] + BALL_RADIUS >= WINDOW_HEIGHT and ball_y_speed > 0:  # check floor collision
        ball_y_speed = -ball_y_speed

    if ball[0] - BALL_RADIUS <= PADDLE_WIDTH and ball[0] >= PADDLE_WIDTH and ball_x_speed < 0 and ball[1] >= \
            left_paddle[1] and ball[1] <= left_paddle[1] + PADDLE_HEIGHT:  # check left paddle collision
        ball_x_speed = -ball_x_speed
        change_ball_color()

        # accelerate ball in left paddle direction of motion
        if left_speed > 0:
            ball_y_speed += 1
        if left_speed < 0:
            ball_y_speed -= 1

    elif ball[0] - BALL_RADIUS <= 0:  # check left wall collision
        right_score += 1
        reset_ball()

    if ball[0] + BALL_RADIUS >= WINDOW_WIDTH - PADDLE_WIDTH and ball[
        0] <= WINDOW_WIDTH - PADDLE_WIDTH and ball_x_speed > 0 and ball[1] >= right_paddle[1] and ball[1] <= \
            right_paddle[1] + PADDLE_HEIGHT:  # check right paddle collision
        ball_x_speed = -ball_x_speed
        change_ball_color()

        # accelerate ball in right paddle direction of motion
        if right_speed > 0:
            ball_y_speed += 1
        if right_speed < 0:
            ball_y_speed -= 1

    elif ball[0] + BALL_RADIUS >= WINDOW_WIDTH:  # check right wall collision
        left_score += 1
        reset_ball()


def create_bullet(side):
    global left_bullets, right_bullets, left_reloaded, right_reloaded, right_goal_epoch, left_goal_epoch

    if side is 'left':
        left_bullets.append([left_gun[0] + GUN_WIDTH, left_gun[1]])
        left_reloaded = False
        left_goal_epoch = time() + RELOAD_TIME

    if side is 'right':
        right_bullets.append([right_gun[0] - GUN_WIDTH, right_gun[1]])
        right_reloaded = False
        right_goal_epoch = time() + RELOAD_TIME


def check_bullet_collision():
    for bullet in left_bullets:
        if bullet[0] + BULLET_WIDTH >= ball[0] - BALL_RADIUS and bullet[0] + BULLET_WIDTH <= ball[0]:
            pass


def reload_bullet():
    global left_reloaded, right_reloaded

    # check if guns have completed reload time
    if time() >= left_goal_epoch and not left_reloaded:
        left_reloaded = True
    if time() >= right_goal_epoch and not right_reloaded:
        right_reloaded = True


def check_paddle_wall_collision():
    global left_speed, right_speed

    # set speed to zero if left paddle is at bottom wall and going down or at top wall and going up
    if (left_paddle[1] < PADDLE_SPEED and left_speed < 0) or \
            (left_paddle[1] >= (WINDOW_HEIGHT - PADDLE_HEIGHT) and left_speed > 0):
        left_speed = 0

    # set speed to zero if right paddle is at bottom wall and going down or at top wall and going up
    if (right_paddle[1] < PADDLE_SPEED and right_speed < 0) or \
            (right_paddle[1] >= (WINDOW_HEIGHT - PADDLE_HEIGHT) and right_speed > 0):
        right_speed = 0


def draw_table():
    global left_paddle, right_paddle, left_speed, right_speed, left_gun, right_gun

    set_clear_color(1, 1, 1)  # set background white
    clear()

    # check for relevant collisions
    check_paddle_wall_collision()
    check_ball_collision()
    reload_bullet()

    # advance paddles, ball, and gun
    right_paddle[1] += right_speed
    left_paddle[1] += left_speed
    ball[0] += ball_x_speed
    ball[1] += ball_y_speed
    left_gun[1] += left_speed
    right_gun[1] += right_speed
    for bullet in left_bullets:
        bullet[0] += BULLET_SPEED
    for bullet in right_bullets:
        bullet[0] -= BULLET_SPEED

    # draw left paddle with gun
    set_fill_color(1, 0, 0)  # red
    draw_rectangle(left_paddle[0], left_paddle[1], PADDLE_WIDTH, PADDLE_HEIGHT)
    draw_rectangle(left_gun[0], left_gun[1], GUN_WIDTH, GUN_HEIGHT)

    # draw right paddle with gun
    set_fill_color(0, 0, 1)  # blue
    draw_rectangle(right_paddle[0], right_paddle[1], PADDLE_WIDTH, PADDLE_HEIGHT)
    draw_rectangle(right_gun[0], right_gun[1], GUN_WIDTH, GUN_HEIGHT)

    # draw ball
    set_fill_color(ball_color[0], ball_color[1], ball_color[2])  # random
    draw_circle(ball[0], ball[1], BALL_RADIUS)

    # draw left players bullets
    set_fill_color(1, 0, 0)  # red
    for bullet in left_bullets:
        draw_rectangle(bullet[0], bullet[1], BULLET_WIDTH, BULLET_HEIGHT)

    # draw right players bullets
    set_fill_color(0, 0, 1)  # blue
    for bullet in right_bullets:
        draw_rectangle(bullet[0], bullet[1], BULLET_WIDTH, BULLET_HEIGHT)

    # draw score
    set_stroke_color(0, 0, 0)  # black
    set_font_bold()
    set_font_size(25)
    draw_text(str(left_score), WINDOW_WIDTH / 3, WINDOW_HEIGHT / 5)
    draw_text(str(right_score), (WINDOW_WIDTH * 2) / 3, WINDOW_HEIGHT / 5)


PADDLE_WIDTH = 10
PADDLE_HEIGHT = 90
PADDLE_SPEED = 5

WINDOW_HEIGHT = 600
WINDOW_WIDTH = 800

LEFT_PADDLE_UP = 'a'
LEFT_PADDLE_DOWN = 'z'
RIGHT_PADDLE_UP = 'k'
RIGHT_PADDLE_DOWN = 'm'
RESET_GAME = ' '
QUIT_GAME = 'q'
LEFT_SHOOT = 'x'
RIGHT_SHOOT = 'l'

BALL_SPEED = 4
BALL_RADIUS = 10

BULLET_WIDTH = 20
BULLET_HEIGHT = 10
BULLET_SPEED = 10

GUN_WIDTH = 15
GUN_HEIGHT = 10
# set ball color randomly, but make sure its never pure white
ball_color = [randint(0, 90) / 100, randint(0, 90) / 100, randint(0, 90) / 100]

left_score = 0
right_score = 0

left_speed = 0
right_speed = 0

# start paddles in middle of their respective goals
left_paddle = [0, (WINDOW_HEIGHT / 2) - (PADDLE_HEIGHT / 2)]  # x and y coords
right_paddle = [WINDOW_WIDTH - PADDLE_WIDTH, (WINDOW_HEIGHT / 2) - (PADDLE_HEIGHT / 2)]  # x and y coords

# create guns in middle of paddles
left_gun = [PADDLE_WIDTH, (WINDOW_HEIGHT / 2) - (GUN_HEIGHT / 2)]
right_gun = [WINDOW_WIDTH - PADDLE_WIDTH - GUN_WIDTH, (WINDOW_HEIGHT / 2) - (GUN_HEIGHT / 2)]

left_bullets = []  # this list will be filled with the coordinates of each of the left players bullets
right_bullets = []  # this list will be filled with the coordinates of each of the left players bullets

RELOAD_TIME = 1  # 1 second reload time
left_reloaded = True
right_reloaded = True

right_goal_epoch = 0
left_goal_epoch = 0

reset_ball()

start_graphics(draw_table, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, key_press=key_pressed)
