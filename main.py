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

def new_ball():
    """
    Make a random ball on the canvas.
    x: random x coord. of circle
    y: random y coord. of circle
    r: radius of circle
    """
    global x, y, r
    canv.delete(ALL)
    x = rnd(100, 700)
    y = rnd(100, 500)
    r = rnd(30, 50)
    canv.create_oval((x - r, y - r), (x + r, y + r),
                     fill = choice(colors), width = 0)
    root.after(1000, new_ball)

def click(event):
    """
    Event handler. Count how far were click from a ball. And if it was
    near then radius from center of circle, count is added one point.
    dif_x_sqrt: x difference between circle coords and click coord
    dif_y_sqrt: y difference between circle coords and click coord
    hypotenuse: distance from click to center of circle
    """
    global count
    dif_x_sqrt = (x - event.x) ** 2
    dif_y_sqrt = (y - event.y) ** 2
    hypotenuse = (dif_x_sqrt + dif_y_sqrt) ** 0.5

    if hypotenuse <= r:
        count += 1
        print('hit', count)


new_ball()
canv.bind('<Button-1>', click)
mainloop()

















