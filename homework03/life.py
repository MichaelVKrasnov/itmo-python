import pathlib
import random
import typing as tp

import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self,
        size: tp.Tuple[int, int],
        randomize: bool = True,
        max_generations: tp.Optional[float] = float("inf"),
    ) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1

    def create_grid(self, randomize: bool = False) -> Grid:
        if randomize:
            return [[random.randint(0, 1) for j in range(0, self.cols)] for i in range(0, self.rows)]
        else:
            return [[0 for j in range(0, self.cols)] for i in range(0, self.rows)]

    def get_neighbours(self, cell: Cell) -> Cells:
        a = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if ((i, j) != (0, 0)) & (i + cell[0] >= 0) & (j + cell[1] >= 0) & (i + cell[0] < self.rows) & (
                        j + cell[1] < self.cols):
                    a.append(self.curr_generation[cell[0] + i][cell[1] + j])
        return a

    def get_next_generation(self) -> Grid:
        new_grid = []
        for i in range(0, self.rows):
            column = []
            for j in range(0, self.cols):
                n = self.get_neighbours((i, j)).count(1)
                if (self.curr_generation[i][j] == 0) & (n == 3):
                    column.append(1)
                elif (self.curr_generation[i][j] == 1) & (n in {2, 3}):
                    column.append(1)
                else:
                    column.append(0)
            new_grid.append(column)
        return new_grid

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        self.prev_generation = [[a for a in list(b)] for b in self.curr_generation]
        self.curr_generation = self.get_next_generation()
        self.generations += 1

    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        return self.generations >= self.max_generations

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        return self.prev_generation != self.curr_generation

    @staticmethod
    def from_file(filename: pathlib.Path, maxgen: float = float("inf")) -> "GameOfLife":
        """
        Прочитать состояние клеток из указанного файла.
        """
        f = open(filename, 'r')
        grid = []
        for i in f:
            column = []
            for j in i[0:-2]:
                column.append(int(j))
            if column:
                grid.append(column)
        f.close()
        game = GameOfLife((len(grid), len(grid[0])), False, maxgen)
        game.curr_generation = grid
        return game

    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        f = open(filename, 'w')
        for i in self.curr_generation:
            s = ""
            for j in i:
                s += str(j)
            f.write(s + "\n")
        f.close()

    def change(self, x: int, y: int) -> None:
        self.curr_generation[x][y] = (self.curr_generation[x][y] + 1) % 2
