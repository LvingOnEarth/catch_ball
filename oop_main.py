import tkinter as tk
from random import randrange as rnd, choice
import math

WIDTH = 800
HEIGHT = 600

root = tk.Tk()
root.geometry(str(WIDTH) + 'x' + str(HEIGHT))

state = True # For start the game again without closing of the main window

canv = tk.Canvas(root, bg = 'white')
canv.pack(fill = 'both', expand = 1)

e = tk.Entry(root, width=20)
l = tk.Label(canv, bg='white', fg='black', width = 20, justify = 'left')
b_start = tk.Button(root, text = 'Старт')
b_finish = tk.Button(root, text = 'Финишь')
b_table = tk.Button(root, text = 'Показать таблицу')

canv.pack(side = 'bottom')
b_finish.pack(side = 'left')
b_start.pack(side = 'left')
b_table.pack(side = 'left')
e.pack(side = 'left')
l.pack(side = 'right')

colors = ['red', 'orange', 'yellow', 'green', 'blue']

# how many hits were
count = 0
figures = []


class Game:
    def __init__(self):
        self.figures = []
        self.state = True
        self.colors = ['red', 'orange', 'yellow', 'green', 'blue']

    def start_game(self, event):
        self.state = True
        player.hits = 0
        e.config(state='disabled')
        l['text'] = ''

        root.bind('<Key>', self.create_figure)
        canv.bind('<Button-1>', self.check_hit)

    def stop_game(self, event):
        self.state = False
        del self.figures
        canv.delete('all')

        player.name = e.get()
        e.config(state='normal')
        e.delete(0, 'end')

        player.write_hits_in_file()

    def create_figure(self, event):
        if event.keysym == '1':
            self.figures.append(Ball(x=rnd(100, 600), y=rnd(100, 400), r=rnd(10, 20),
                             dx=rnd(1, 5), dy=rnd(1, 5), color=choice(self.colors)))
        elif event.keysym == '2':
            self.figures.append(Triangle(x=rnd(100, 600), y=rnd(100, 400), r=rnd(50, 100),
                             dx=rnd(1, 5), dy=rnd(1, 5), start_angle=0, d_angle=0, color=choice(self.colors)))

    def check_hit(self, event):
        if len(self.figures) > 0:
            for figure in self.figures:
                hit = figure.check_hit(event.x, event.y)
                player.count_hits(hit)

    def show_table_of_hits(self, event):
        with open('best_players.txt', 'r') as hand:
            table = hand.read()

        l['text'] = table

    def tick(self):
        if self.state == True:
            for figure in game.figures:
                figure.move()
                figure.show()

            root.after(50, self.tick)


class Player:
    def __init__(self, name, hits):
        self.name = name
        self.hits = hits
        self.players = []

    def count_hits(self, numb_of_hit):
        self.hits += numb_of_hit

    def write_hits_in_file(self):
        with open('best_players.txt', 'r') as handle:
            self.players = handle.readlines()

        self.players = self.check_same_name_in_file()

        if len(self.players) > 1:
            self.players = self.sort_players_in_file()

        with open('best_players.txt', 'w') as file_handler:
            file_handler.writelines(self.players)

    def check_same_name_in_file(self):
        if len(self.players) == 0:
            self.players.append(str(self.hits) + ' - ' + self.name + '\n')
            return self.players

        for i in range(len(self.players)):
            if self.players[i].endswith(self.name + '\n'):
                spl = self.players[i].split(' - ')
                if self.hits >= int(spl[0]):
                    self.players[i] = str(self.hits) + ' - ' + self.name + '\n'
                return self.players

        self.players.append(str(self.hits) + ' - ' + self.name + '\n')
        return self.players

    def sort_players_in_file(self):
        arr_players = []

        for player in self.players:
            arr_players.append(player.split(' - '))

        for player in arr_players:
            player[0] = int(player[0])

        arr_players.sort()

        finish_arr = [(str(player[0]) + ' - ' + player[1]) for player in arr_players]

        return finish_arr


class Ball:
    def __init__(self, x, y, r, dx, dy, color):
        self.x = x
        self.y = y
        self.r = r
        self.dx = dx
        self.dy = dy
        self.color = color
        self.id_ball = canv.create_oval((self.x - self.r), (self.y - self.r),
                                        (self.x + self.r), (self.y + self.r),
                                        fill = self.color)

    def show(self):
        canv.move(self.id_ball, self.dx, self.dy)

    def move(self):
        self.x += self.dx
        self.y += self.dy

        self.check_collision_walls()

    def check_collision_walls(self):
        if (self.x + self.r >= WIDTH) or (self.x - self.r <= 0):
            self.dx *= (-1)
        elif (self.y + self.r >= HEIGHT) or (self.y - self.r <= 0):
            self.dy *= (-1)

    def check_collision_figures(self):
        pass

    def check_hit(self, event_x, event_y):
        kat_x = (event_x - self.x) ** 2
        kat_y = (event_y - self.y) ** 2
        hypotenuse = (kat_x + kat_y) ** 0.5

        if self.r >= hypotenuse:
            return 1
        else:
            return 0


class Triangle:
    def __init__(self, x, y, r, dx, dy, start_angle, d_angle, color):
        self.x = x
        self.y = y
        self.r = r
        self.dx = dx
        self.dy = dy
        self.start_angle = start_angle
        self.d_angle = d_angle
        self.coords = []
        self.color = color
        self.id_triangle = ''

    def create_triangle(self):
        return self.move()

    def show(self):
        canv.delete(self.id_triangle)
        self.id_triangle = canv.create_polygon((self.coords[0], self.coords[3]),
                                               (self.coords[1], self.coords[4]),
                                               (self.coords[2], self.coords[5]), fill=self.color)

    def move(self):
        x1 = self.x + (self.r * math.sin(self.start_angle * (math.pi / 180)))
        y1 = self.y - (self.r * math.cos(self.start_angle * (math.pi / 180)))

        x2 = self.x - (self.r * math.sin((60 + self.start_angle) * (math.pi / 180)))
        y2 = self.y + (self.r * math.cos((60 + self.start_angle) * (math.pi / 180)))

        x3 = self.x + (self.r * math.sin((60 - self.start_angle) * (math.pi / 180)))
        y3 = self.y + (self.r * math.cos((60 - self.start_angle) * (math.pi / 180)))

        self.coords = [x1, x2, x3, y1, y2, y3]

        collision_x = self.check_collision_walls(WIDTH, [x1, x2, x3])
        collision_y = self.check_collision_walls(HEIGHT, [y1, y2, y3])

        if collision_x:
            self.dx *= (-1)
            self.x += self.dx * 2  # prevent sticking figure in the walls
            self.d_angle = -1
        elif collision_y:
            self.dy *= (-1)
            self.y += self.dy * 2  # prevent sticking figure in the walls
            self.d_angle = 1

        # collision_with_figures = check_collision_with_figures(triangle)

        self.x += self.dx
        self.y += self.dy
        self.start_angle += self.d_angle

        if (self.start_angle == 120) or (self.start_angle == -120):
            self.start_angle = 0


    def check_collision_walls(self, hor_ver, coords):
        for i in range(len(coords)):
            if (coords[i] >= hor_ver) or (coords[i] <= 0):
                return True

    def check_collision_figures(self):
        pass

    def check_hit(self, event_x, event_y):
        pos_start_angle = self.start_angle * (-1)
        h = self.r / 2
        r = 0

        kat_x = event_x - self.x
        kat_y = event_y - self.y
        hypotenuse = (kat_x ** 2 + kat_y ** 2) ** 0.5

        cos_alpha = math.fabs(kat_x) / hypotenuse
        angle = math.acos(cos_alpha) * (180 / math.pi)

        if self.start_angle >= 0:
            if (kat_x >= 0) and (kat_y < 0):
                if angle <= (90 - self.start_angle):
                    r = h / math.cos((angle - (30 - self.start_angle)) * (math.pi / 180))
                else:
                    r = h / math.cos(math.fabs((90 - angle) + (90 - (30 + self.start_angle))) * (math.pi / 180))

            elif (kat_x <= 0) and (kat_y < 0):
                if self.start_angle > 30:
                    if angle >= (self.start_angle - 30):
                        r = h / math.cos(((self.start_angle + 30) - angle) * (math.pi / 180))
                    else:
                        r = h / math.cos((math.fabs(angle + (90 - self.start_angle))) * (math.pi / 180))
                else:
                    r = h / math.cos(math.fabs(angle - (30 + self.start_angle)) * (math.pi / 180))

            elif (kat_x <= 0) and (kat_y > 0):
                if self.start_angle < 30:
                    if angle < (30 - self.start_angle):
                        r = h / math.cos(((30 + self.start_angle) + angle) * (math.pi / 180))
                    else:
                        r = h / math.cos(((90 - self.start_angle) - angle) * (math.pi / 180))
                elif self.start_angle <= 60:
                    r = h / math.cos(math.fabs((90 - self.start_angle) - angle) * (math.pi / 180))
                else:
                    if angle < (90 - (self.start_angle - 60)):
                        r = h / math.cos(math.fabs((90 - self.start_angle) - angle) * (math.pi / 180))
                    else:
                        r = h / math.cos(((90 - (self.start_angle - 30)) + (90 - angle)) * (math.pi / 180))

            elif (kat_x >= 0) and (kat_y > 0):
                if self.start_angle <= 60:
                    if angle > (self.start_angle + 30):
                        r = h / math.cos((self.start_angle + (90 - angle)) * (math.pi / 180))
                    else:
                        if self.start_angle <= 30:
                            r = h / math.cos(((30 - self.start_angle) + angle) * (math.pi / 180))
                        else:
                            r = h / math.cos((angle - (self.start_angle - 30)) * (math.pi / 180))

                elif self.start_angle <= 90:
                    r = h / math.cos(math.fabs(angle - (self.start_angle - 30)) * (math.pi / 180))

                else:
                    if angle <= (self.start_angle - 90):
                        r = h / math.cos(((90 - (self.start_angle - 60)) + angle) * (math.pi / 180))
                    else:
                        r = h / math.cos(math.fabs(angle - (self.start_angle - 30)) * (math.pi / 180))

        elif self.start_angle < 0:
            if (kat_x >= 0) and (kat_y < 0):
                if pos_start_angle > 30:
                    if angle >= (pos_start_angle - 30):
                        r = h / math.cos(((pos_start_angle + 30) - angle) * (math.pi / 180))
                    else:
                        r = h / math.cos((math.fabs(angle + (90 - pos_start_angle))) * (math.pi / 180))
                else:
                    r = h / math.cos(math.fabs(angle - (30 + pos_start_angle)) * (math.pi / 180))

            elif (kat_x <= 0) and (kat_y < 0):
                if angle <= (90 - pos_start_angle):
                    r = h / math.cos((angle - (30 - pos_start_angle)) * (math.pi / 180))
                else:
                    r = h / math.cos(math.fabs((90 - angle) + (90 - (30 + pos_start_angle))) * (math.pi / 180))

            elif (kat_x <= 0) and (kat_y > 0):
                if pos_start_angle <= 60:
                    if angle > (pos_start_angle + 30):
                        r = h / math.cos((pos_start_angle + (90 - angle)) * (math.pi / 180))
                    else:
                        if pos_start_angle <= 30:
                            r = h / math.cos(((30 - pos_start_angle) + angle) * (math.pi / 180))
                        else:
                            r = h / math.cos((angle - (pos_start_angle - 30)) * (math.pi / 180))

                elif pos_start_angle <= 90:
                    r = h / math.cos(math.fabs(angle - (pos_start_angle - 30)) * (math.pi / 180))

                else:
                    if angle <= (pos_start_angle - 90):
                        r = h / math.cos(((90 - (pos_start_angle - 60)) + angle) * (math.pi / 180))
                    else:
                        r = h / math.cos(math.fabs(angle - (pos_start_angle - 30)) * (math.pi / 180))

            elif (kat_x >= 0) and (kat_y >= 0):
                if pos_start_angle < 30:
                    if angle < (30 - pos_start_angle):
                        r = h / math.cos(((30 + pos_start_angle) + angle) * (math.pi / 180))
                    else:
                        r = h / math.cos(((90 - pos_start_angle) - angle) * (math.pi / 180))
                elif pos_start_angle <= 60:
                    r = h / math.cos(math.fabs((90 - pos_start_angle) - angle) * (math.pi / 180))
                else:
                    if angle < (90 - (pos_start_angle - 60)):
                        r = h / math.cos(math.fabs((90 - pos_start_angle) - angle) * (math.pi / 180))
                    else:
                        r = h / math.cos(((90 - (pos_start_angle - 30)) + (90 - angle)) * (math.pi / 180))

        if hypotenuse <= math.fabs(r):
            return 3
        else:
            return 0


game = Game()
player = Player('Aleksandr', 0)

root.bind('<Return>', game.start_game)
b_start.bind('<Button-1>', game.start_game)
b_finish.bind('<Button-1>', game.stop_game)
b_table.bind('<Button-1>', game.show_table_of_hits)
game.tick()

tk.mainloop()

# improve collision of figures between each others
# def check_collision_with_figures(figure):
#     if figure[0] == 'ball':
#         for item in figures:
#             if figure == item:
#                 continue
#
#             dist_x = (item[1] - figure[1]) ** 2
#             dist_y = (item[2] - figure[2]) ** 2
#             hypo = (dist_x + dist_y) ** 0.5
#
#             distance_between_figures = hypo - (item[5] + figure[5])
#
#             if distance_between_figures >= figure[3]:
#                 continue
#             elif distance_between_figures <= 0:
#                 return True



















