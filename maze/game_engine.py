from maze.maze_entities import Player


class Pacgame:
    def __init__(self, x, y, px, py):
        self.cell_x, self.cell_y = x, y
        self.px, self.py = px, py

class SuperPacgame(Pacgame):
    pass

class Engine:
    def __init__(self):
        self.pacgame_eated = 0
        self.superpacgame_eated = 0
