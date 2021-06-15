import random
import typing as tp

import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self, width: int = 640, height: int = 480, cell_size: int = 10, speed: int = 10
    ) -> None:
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed

    def draw_lines(self) -> None:
        """ Отрисовать сетку """
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def run(self) -> None:
        """ Запустить игру """
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))

        self.grid = self.create_grid(True)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False

            self.draw_grid()
            self.draw_lines()
            self.grid = self.get_next_generation()

            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def create_grid(self, randomize: bool = False) -> Grid:
        """
        Создание списка клеток.

        Клетка считается живой, если ее значение равно 1, в противном случае клетка
        считается мертвой, то есть, ее значение равно 0.

        Parameters
        ----------
        randomize : bool
            Если значение истина, то создается матрица, где каждая клетка может
            быть равновероятно живой или мертвой, иначе все клетки создаются мертвыми.

        Returns
        ----------
        out : Grid
            Матрица клеток размером `cell_height` х `cell_width`.
        """
        if randomize:
            return [[random.randint(0, 1) for j in range(0, self.width // self.cell_size)] for i in
                    range(0, self.height // self.cell_size)]
        else:
            return [[0 for j in range(0, self.cell_width)] for i in range(0, self.cell_height)]

    def draw_grid(self) -> None:
        """
        Отрисовка списка клеток с закрашиванием их в соответствующе цвета.
        """
        cs = self.cell_size

        for i in range(0, self.cell_height):
            for j in range(0, self.cell_width):
                if self.grid[i][j] == 1:
                    pygame.draw.rect(self.screen, pygame.Color('green'), (cs * j, cs * i, cs, cs))
                else:
                    pygame.draw.rect(self.screen, pygame.Color('white'), (cs * j, cs * i, cs, cs))

    def get_neighbours(self, cell: Cell) -> Cells:
        """
        Вернуть список соседних клеток для клетки `cell`.

        Соседними считаются клетки по горизонтали, вертикали и диагоналям,
        то есть, во всех направлениях.

        Parameters
        ----------
        cell : Cell
            Клетка, для которой необходимо получить список соседей. Клетка
            представлена кортежем, содержащим ее координаты на игровом поле.

        Returns
        ----------
        out : Cells
            Список соседних клеток.
        """
        a = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if ((i, j) != (0, 0)) & (i + cell[0] >= 0) & (j + cell[1] >= 0) & (i + cell[0] < self.cell_height) & (
                        j + cell[1] < self.cell_width):
                    a.append(self.grid[cell[0] + i][cell[1] + j])
        return a

    def get_next_generation(self) -> Grid:
        """
        Получить следующее поколение клеток.

        Returns
        ----------
        out : Grid
            Новое поколение клеток.
        """
        new_grid = []
        for i in range(0, self.cell_height):
            column = []
            for j in range(0, self.cell_width):
                n = 0
                for e in self.get_neighbours((i, j)):
                    if e == 1:
                        n += 1
                if (self.grid[i][j] == 0) & (n == 3):
                    column.append(1)
                elif (self.grid[i][j] == 1) & (n in {2, 3}):
                    column.append(1)
                else:
                    column.append(0)
            new_grid.append(column)
        return new_grid


game = GameOfLife()
game.run()
