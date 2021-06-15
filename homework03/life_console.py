import curses
import pathlib
import sys

from life import GameOfLife
from ui import UI
from local import *


class Console(UI):
    def __init__(self, life: GameOfLife, speed: int) -> None:
        super().__init__(life)
        self.speed = speed

    def draw_borders(self, screen) -> None:
        """ Отобразить рамку. """
        screen.addstr(0, 0, CONTROL_CONSOLE)
        x = self.life.cols
        y = self.life.rows
        for k in range(0, x + 4):
            for j in range(0, y + 4):
                if ((k == 2) | (k == x + 3)) & ((j == 1) | (j == y + 2)) & (k > 1) & (k < x + 4) & (j > 0) & (
                        j < y + 3):
                    screen.addch(k, j, ord("+"))
                elif ((k == 2) | (k == x + 3)) & (k > 1) & (k < x + 4) & (j > 0) & (j < y + 3):
                    screen.addch(k, j, ord("-"))
                elif ((j == 1) | (j == y + 2)) & (k > 1) & (k < x + 4) & (j > 0) & (j < y + 3):
                    screen.addch(k, j, ord("|"))

    def draw_grid(self, screen) -> None:
        """ Отобразить состояние клеток. """
        screen.move(1, 1)
        for k in range(0, self.life.cols):
            for j in range(0, self.life.rows):
                if self.life.curr_generation[j][k] == 1:
                    screen.addch(k + 3, j + 2, ord("#"))
                else:
                    screen.addch(k + 3, j + 2, " ")
        screen.move(0, 0)

    def run(self) -> None:
        screen = curses.initscr()
        try:
            self.draw_borders(screen)
        except curses.error:
            print(GRID_TOO_BIG)
            quit(-1)
        screen.nodelay(True)
        running = True
        while running:
            self.draw_grid(screen)
            self.life.step()
            screen.refresh()
            screen.move(0, 0)
            curses.napms(self.speed)
            c = screen.getch()
            if self.life.is_max_generations_exceeded:
                running = False
            if c == ord("q"):
                running = False
            elif c == ord("s"):
                curses.endwin()
                print(SAVE)
                s = input()
                if s != "":
                    self.life.save(pathlib.Path(s))
                screen = curses.initscr()
                self.draw_borders(screen)
            else:
                self.draw_borders(screen)
        curses.endwin()


i = 1
args = sys.argv
width = 30
height = 7
random = False
help = False
file = None
speed = 100
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
    print(HELP_SPEED)
    print(HELP_HEIGHT)
    print(HELP_RANDOM)
    print(HELP_FROMFILE)
    print(HELP_MAXGEN)
else:
    print(WELCOME_CONSOLE)
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
    print(SETTINGS_SPEED, speed)
    if not mg == float("inf"):
        print(SETTINGS_MAXGEN, mg)
    print()
    print(HELP_INFORM)
    if speed > 10000:
        print(SPEED_TOO_BIG)
    if file is None:
        simulator = GameOfLife((width, height), random, mg)
    else:
        simulator = GameOfLife.from_file(file, mg)
    ui = Console(simulator, speed)
    ui.run()
