import string
from random import sample, randint, choice
from itertools import cycle

import pygame as pg

import prepare
from animation import Task


class Cell(object):
    def __init__(self, index, cell_size, top_offset, color):
        self.index = index
        self.value = None
        self.age = 0
        self.highlight = 0
        self.color = color
        x, y = index
        w, h = cell_size
        self.rect = pg.Rect(x * w, (y * h) - top_offset, w, h)


class Grid(object):
    def __init__(self):
        self.cell_size = (20, 24)
        self.age_limit = 60
        self.num_columns = 64
        self.num_rows = 32
        self.top_offset = 2 * self.cell_size[1]
        self.min_alive = 64
        self.colors = cycle(("green", "teal", "blue", "purple",
                                      "pink", "red", "orange", "yellow"))
        self.color = next(self.colors)

        self.make_cells()
        self.make_images()
        self.animations = pg.sprite.Group()
        task = Task(self.next_color, 10000, -1)
        self.animations.add(task)

    def next_color(self):
        self.color = next(self.colors)

    def make_cells(self):
        self.cells = {}
        self.columns = {}
        for x in range(self.num_columns):
            self.columns[x] = []
            for y in range(self.num_rows):
                cell = Cell((x, y), self.cell_size, self.top_offset, self.color)
                self.cells[(x, y)] = cell
                self.columns[x].append(cell)

    def make_images(self):
        colors = {"green": pg.Color(50, 168, 50),
                       "teal": pg.Color(50, 168, 139),
                       "blue": pg.Color(50, 109, 168),
                       "purple": pg.Color(80, 50, 168),
                       "pink": pg.Color(168, 50, 168),
                       "red": pg.Color(168, 50, 80),
                       "orange": pg.Color(168, 109, 50),
                       "yellow": pg.Color(139, 168, 50)}

        font = pg.font.Font(prepare.FONTS["matrix-code-nfi"], 26)
        self.images = {}
        self.highlights = {}
        p = "".join((x for x in string.punctuation if x not in "@`"))
        chars = string.lowercase + string.digits + p
        self.num_chars = len(chars)
        for color in colors:
            c = colors[color]
            self.images[color] = {}
            for num, char in enumerate(chars):
                full_img = font.render("{}".format(char), True, c, pg.Color("black"))
                highlight = font.render("{}".format(char), True,
                                                  pg.Color(157, 163, 148), pg.Color("black"))
                self.images[color][num] = {}
                self.highlights[num] = {}
                for alpha in range(256):
                    img = full_img.copy()
                    img.set_alpha(alpha)
                    h_img = highlight.copy()
                    h_img.set_alpha(alpha)
                    w, h = img.get_size()
                    self.images[color][num][alpha] = img
                    self.highlights[num][alpha] = h_img

    def update_cell(self, cell_index):
        cell = self.cells[cell_index]
        if cell.highlight > 0:
            cell.highlight -= 35
        if cell.highlight < 0:
            cell.highlight = 0
        x, y = cell_index
        if cell.age:
            if cell.age < 45:
                flip_chance = randint(1, 100)
                if flip_chance < 5:
                    self.new_vals[cell.index] = randint(0, self.num_chars - 1)
        else:
            try:
                neighbor = self.cells[(x, y - 1)]
            except KeyError:
                neighbor = None
            if neighbor is not None and neighbor.age:
                self.new_cells.append((cell.index, randint(0, self.num_chars - 1)))
                cell.highlight = 220
                cell.color = neighbor.color
        if cell.age:
            cell.age += 1
        if cell.age > self.age_limit:
            cell.age = 0

    def spawn(self):
        empty = []
        for c in self.columns.values():
            if all((not x.age for x in c[0:self.num_rows + 1])):
                empty.append(c)
        for column in empty:
            if randint(1, 100) < 5:
                cell = column[0]
                cell.color = self.color
                self.new_cells.append((cell.index, randint(0, self.num_chars - 1)))

    def update(self, dt):
        self.animations.update(dt)
        self.new_vals = {}
        self.new_cells = []
        for cell_index in self.cells.keys():
            self.update_cell(cell_index)
        for i in self.new_vals:
            self.cells[i].value = self.new_vals[i]
        self.spawn()
        for new_i, value in self.new_cells:
            c = self.cells[new_i]
            c.value = value
            c.age = 1

    def draw_cells(self, surface):
        for cell in self.cells.values():
            if cell.age:
                alpha = int(255 - ((cell.age / float(self.age_limit)) * 255))
                surface.blit(self.images[cell.color][cell.value][alpha], cell.rect)
                if cell.highlight:
                    surface.blit(self.highlights[cell.value][cell.highlight], cell.rect)

    def draw(self, surface):
        surface.fill(pg.Color("black"))
        self.draw_cells(surface)
