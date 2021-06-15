import pathlib

import pygame
import sys
from life import GameOfLife
from pygame.locals import *
from ui import UI
from local import *


class GUI(UI):
    def __init__(self, life: GameOfLife, cell_size: int = 10, speed: int = 10) -> None:
        super().__init__(life)
        self.cell_size = cell_size
        self.speed = speed
        self.screen = pygame.display.set_mode((life.rows * cell_size, life.cols * cell_size))

    def draw_lines(self) -> None:
        for x in range(0, self.life.rows):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (x * self.cell_size, 0), (x * self.cell_size, self.life.cols * self.cell_size))
        for y in range(0, self.life.cols):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (0, y * self.cell_size), (self.life.rows * self.cell_size, y * self.cell_size))

    def draw_grid(self) -> None:
        cs = self.cell_size
        for k in range(0, self.life.rows):
            for j in range(0, self.life.cols):
                if self.life.curr_generation[k][j] == 1:
                    pygame.draw.rect(self.screen, pygame.Color('green'), (cs * k, cs * j, cs, cs))
                else:
                    pygame.draw.rect(self.screen, pygame.Color('white'), (cs * k, cs * j, cs, cs))

    def run(self) -> None:
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))

        running = True
        pause = False
        while running:
            self.draw_grid()
            self.draw_lines()
            pygame.display.flip()
            if self.life.is_max_generations_exceeded:
                running = False
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        pause = not pause
                    elif event.key == K_s:
                        running = False
                        print(SAVE)
                        s = input()
                        if s != "":
                            self.life.save(pathlib.Path(s))
                elif (event.type == MOUSEBUTTONDOWN) & pause:
                    x = event.pos[0] // self.cell_size
                    y = event.pos[1] // self.cell_size
                    self.life.change(x, y)
            if not pause:
                clock.tick(self.speed)
                self.life.step()
        pygame.quit()


i = 1
args = sys.argv
width = 30
height = 20
random = False
cell_size = 10
speed = 10
help = False
file = None
mg = float("inf")

while len(args) > i:
    if (args[i] == "--help") | (args[i] == "-h"):
        help = True
    if (args[i] == "--width") | (args[i] == "-w"):
        i += 1
        width = int(args[i])
    elif (args[i] == "--height") | (args[i] == "-H"):
        i += 1
        height = int(args[i])
    elif (args[i] == "--randomize") | (args[i] == "-r"):
        random = True
    elif (args[i] == "--cell_size") | (args[i] == "-c"):
        i += 1
        cell_size = int(args[i])
    elif (args[i] == "--speed") | (args[i] == "-s"):
        i += 1
        speed = int(args[i])
    elif (args[i] == "--maxgen") | (args[i] == "-m"):
        i += 1
        mg = int(args[i])
    elif (args[i] == "--from_file") | (args[i] == "-l"):
        i += 1
        file = args[i]
    i += 1

if help:
    print(HELP_INTRO)
    print(HELP_HELP)
    print(HELP_WIDTH)
    print(HELP_HEIGHT)
    print(HELP_RANDOM)
    print(HELP_CELLSIZE)
    print(HELP_SPEED)
    print(HELP_FROMFILE)
    print(HELP_MAXGEN)
else:
    print(WELCOME_GUI)
    print()
    print(SETTINGS_INTRO)
    print()
    if file is not None:
        print(SETTINGS_SOURCE, file)
    else:
        if random:
            print(SETTINGS_SOURCE_RANDOM)
        else:
            print(SETTINGS_SOURCE_EMPTY)
        print(SETTINGS_WIDTH, width)
        print(SETTINGS_HEIGHT, height)
    print(SETTINGS_CELLSIZE, cell_size)
    print(SETTINGS_SPEED, speed)
    if not mg == float("inf"):
        print(SETTINGS_MAXGEN, mg)
    print()
    print(HELP_INFORM)
    print(CONTROL_GUI)
    if file is None:
        simulator = GameOfLife((width, height), random, mg)
    else:
        simulator = GameOfLife.from_file(pathlib.Path(file), mg)
    ui = GUI(simulator, cell_size, speed)
    ui.run()
