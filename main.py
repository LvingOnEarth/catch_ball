from tkinter import *
from random import randrange as rnd, choice
import time

root = Tk()
root.geometry('800x600')

canv = Canvas(root, bg = 'white')
canv.pack(fill = BOTH, expand = 1)

colors = ['red', 'orange', 'yellow', 'green', 'blue']

# how many hits were
count = 0

balls = []

def new_ball():
    """
    Make a random ball on the canvas.
    x: random x coord. of circle
    y: random y coord. of circle
    r: radius of circle
    """
    ball = []
    x = rnd(100, 700)
    y = rnd(100, 500)
    r = rnd(30, 50)
    color = choice(colors)

    dx, dy = calc_speed()
    ball.append(x)
    ball.append(y)
    ball.append(r)
    ball.append(dx)
    ball.append(dy)
    ball.append(color)

    balls.append(ball)

    move_ball()

def calc_speed():
    dx = rnd(1, 5)
    dy = rnd(1, 5)
    return dx, dy

def move_ball():
    canv.delete(ALL)

    for i in range(len(balls)):
        if ((balls[i][0] - balls[i][2]) <= 0):
            balls[i][3] *= (-1)
        elif ((balls[i][1] - balls[i][2]) <= 0):
            balls[i][4] *= (-1)
        elif ((balls[i][0] + balls[i][2]) >= 800):
            balls[i][3] *= (-1)
        elif ((balls[i][1] + balls[i][2]) >= 600):
            balls[i][4] *= (-1)

        balls[i][0] += balls[i][3]
        balls[i][1] += balls[i][4]

        draw_ball(balls[i][0], balls[i][1], balls[i][2], balls[i][5])

    root.after(50, move_ball)

def draw_ball(x, y, r, color):
    canv.create_oval((x - r, y - r), (x + r, y + r),
                     fill=color, width=0)

def click_new_ball(event):
    new_ball()

def click_hit(event):
    """
    Event handler. Count how far were click from a ball. And if it was near then radius from center of circle, count is added one point.
    dif_x_sqrt: x difference between circle coords and click coord
    dif_y_sqrt: y difference between circle coords and click coord
    hypotenuse: distance from click to center of circle
    """
    global count

    for i in range(len(balls)):
        dif_x_sqrt = (balls[i][0] - event.x) ** 2
        dif_y_sqrt = (balls[i][1] - event.y) ** 2
        hypotenuse = (dif_x_sqrt + dif_y_sqrt) ** 0.5

        if hypotenuse <= balls[i][2]:
            count += 1
            print(balls[i][5], count)

canv.bind('<Button-1>', click_new_ball)
canv.bind('<Button-3>', click_hit)
mainloop()


















