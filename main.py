from tkinter import *
from random import randrange as rnd, choice
# import line
import math
import time

root = Tk()
root.geometry('800x600')

canv = Canvas(root, bg = 'white')
canv.pack(fill = BOTH, expand = 1)

colors = ['red', 'orange', 'yellow', 'green', 'blue']

# how many hits were
count = 0

balls = []
figures = []

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

    speed = calc_speed('ball')
    ball.append(x)
    ball.append(y)
    ball.append(r)
    ball.append(speed[0])
    ball.append(speed[1])
    ball.append(color)

    balls.append(ball)

    move_ball()

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

def check_length(figure):
    dif_x_sqrt = (figure[0] - figure[2]) ** 2
    dif_y_sqrt = (figure[1] - figure[3]) ** 2
    hypotenuse = (dif_x_sqrt + dif_y_sqrt) ** 0.5

    if hypotenuse > figure[8]:
        return True
    else:
        return False

def calc_speed(figure):
    speed = []

    if figure == 'ball':
        dx = rnd(1, 5)
        dy = rnd(1, 5)
        speed.append(dx)
        speed.append(dy)

    elif figure == 'line':
        dx1 = rnd(1, 5)
        dy1 = rnd(1, 5)
        d_angle = 0
        speed.append(dx1)
        speed.append(dy1)
        speed.append(d_angle)

    elif figure == 'triangle':
        dx = rnd(5, 10)
        dy = rnd(5, 10)
        speed.append(dx)
        speed.append(dy)

    return speed


def new_figure():
    figure = []
    x1 = rnd(100, 600)
    y1 = rnd(100, 400)
    angle = rnd(10, 80)
    r = 100

    x2 = x1 + (r * math.cos((90 - angle) * (math.pi / 180)))
    y2 = y1 + (r * math.cos(angle * (math.pi / 180)))

    speed = calc_speed('line')

    figure.append(x1)
    figure.append(y1)
    figure.append(x2)
    figure.append(y2)
    figure.append(speed[0])
    figure.append(speed[1])
    figure.append(speed[2])
    figure.append(r)
    figure.append(angle)

    figures.append(figure)

    move_figure()


def move_figure():
    """
    0: x1; 1: y1; 2: x2; 3: y2
    4: dx1; 5: dy1; 6: d_angle 7: r; 8: angle;
    """
    canv.delete(ALL)

    state = ''

    for i in range(len(figures)):
        if (figures[i][0] <= 0) or (figures[i][0] >= 800):
            figures[i][4] *= (-1)
            state = 'first'
        elif (figures[i][1] <= 0) or (figures[i][1] >= 600):
            figures[i][5] *= (-1)
            state = 'first'

        if (figures[i][2] <= 0) or (figures[i][2] >= 800):
            if figures[i][2] >= figures[i][0]:
                figures[i][6] = 0.5
            else:
                figures[i][6] = -0.5
            figures[i][4] *= (-1)
            state = 'second'
        elif (figures[i][3] <= 0) or (figures[i][3] >= 600):
            if figures[i][3] >= figures[i][1]:
                figures[i][6] = -0.5
            else:
                figures[i][6] = 0.5
            figures[i][5] *= (-1)
            state = 'second'

        # calculate new coord
        figure_new_coord = calc_new_point(figures[i], state)

        draw_figure(figure_new_coord[0], figure_new_coord[1], figure_new_coord[2], figure_new_coord[3])

    root.after(50, move_figure)

def calc_new_point(figure, state):
    if state == 'first':
        figure[8] += figure[6]  # change angle
        figure[0] += figure[4]  # change x1
        figure[1] += figure[5]  # change y1
        figure[2] = figure[0] + (figure[7] * math.cos((90 - figure[8]) * (math.pi / 180)))  # change x2
        figure[3] = figure[1] + (figure[7] * math.cos(figure[8] * (math.pi / 180)))  # change y2
    elif state == 'second':
        figure[8] += figure[6]  # change angle
        figure[2] += figure[4]  # change x2
        figure[3] += figure[5]  # change y2
        figure[0] = figure[2] - (figure[7] * math.cos((90 - figure[8]) * (math.pi / 180)))  # change x1
        figure[1] = figure[3] - (figure[7] * math.cos(figure[8] * (math.pi / 180)))  # change y1
    elif state == '':
        figure[8] += figure[6]  # change angle
        figure[0] += figure[4]  # change x1
        figure[1] += figure[5]  # change y1
        figure[2] = figure[0] + (figure[7] * math.cos((90 - figure[8]) * (math.pi / 180)))  # change x2
        figure[3] = figure[1] + (figure[7] * math.cos(figure[8] * (math.pi / 180)))  # change y2

    return figure


def draw_figure(x1, y1, x2, y2):
    canv.create_line((x1, y1), (x2, y2),
                     fill='green', width=5)




def new_triangle():


    triangle = []

    x = rnd(100, 600)
    y = rnd(100, 400)
    r = 50
    angle = 30
    color = choice(colors)
    speed = calc_speed('triangle')

    triangle.append(x)
    triangle.append(y)
    triangle.append(r)
    triangle.append(angle)
    triangle.append(color)
    triangle.append(speed[0])
    triangle.append(speed[1])

    figures.append(triangle)

    triangle_coord = calc_point_triangle(x, y, r, angle)
    move_triangle(triangle_coord)

def move_triangle(triangle_coord):
    canv.delete(ALL)

    for i in range(len(figures)):
        if triangle_coord[4] >= 800 or triangle_coord[0] <= 0:
            figures[i][5] *= (-1)
        elif triangle_coord[5] >= 600 or triangle_coord[3] <= 0:
            figures[i][6] *= (-1)

        figures[i][0] += figures[i][5]
        figures[i][1] += figures[i][6]
        triangle_coord = calc_point_triangle(figures[i][0], figures[i][1], figures[i][2], figures[i][3])
        draw_triangle(triangle_coord, figures[i][4])

    root.after(50, move_triangle, triangle_coord)

def calc_point_triangle(x, y, r, angle):
    x1 = round(x - r * math.cos(angle * (math.pi / 180)))
    y1 = round(y + r * math.sin(angle * (math.pi / 180)))

    x2 = x
    y2 = y - r

    x3 = round(x + r * math.cos(angle * (math.pi / 180)))
    y3 = round(y + r * math.sin(angle * (math.pi / 180)))

    return [x1, y1, x2, y2, x3, y3]

def draw_triangle(triangle_coord, color):
    canv.create_polygon((triangle_coord[0], triangle_coord[1]),
                        (triangle_coord[2], triangle_coord[3]),
                        (triangle_coord[4], triangle_coord[5]),
                        fill = color)





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

def click_new_figure(event):
    new_figure()

def click_triangle(event):
    new_triangle()

canv.bind('<Button-1>', click_new_ball)
canv.bind('<Button-3>', click_triangle)
# canv.bind('<Button-3>', click_new_figure)
# canv.bind('<Button-3>', click_hit)
mainloop()


















