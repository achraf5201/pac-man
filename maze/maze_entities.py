import arcade
from maze.maze_adapter import MazeAdapter


class Entity:
    pass


class Player:
    def __init__(self, x, y, pixel_x, pixel_y, speed, maze_adapter):
        self.cell_x = x
        self.cell_y = y
        self.pixel_x = pixel_x
        self.pixel_y = pixel_y
        self.speed = speed
        self.maze_adapter = maze_adapter

        self.current_dir = None
        self.next_dir = None

        self.target_cell_x = x
        self.target_cell_y = y
        self.target_px = pixel_x
        self.target_py = pixel_y

        self.start_angle = 20
        self.end_angle = 340
        self.flag = 1

    def get_cor(self, direction):
        if direction == 1:
            return 0, -1
        elif direction == 2:
            return 1, 0
        elif direction == 4:
            return 0, 1
        elif direction == 8:
            return -1, 0
        return 0, 0

    def update(self, delta_time):
        if self.flag == 1:
            self.start_angle += 120 * delta_time
            self.end_angle -= 120 * delta_time
            if self.start_angle >= 45:
                self.flag = 0
        else:
            self.start_angle -= 120 * delta_time
            self.end_angle += 120 * delta_time
            if self.start_angle <= 5:
                self.flag = 1



class Ghost(Entity):
    pass


class EntityManager:
    pass
