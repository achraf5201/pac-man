import random
from collections import deque
import sys


class Ghost:
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

        self.path = []

        self.chase = False
        self.run = False
        self.random_move = True

        self.seen = deque()

        self.range = []

    def _update_range(self):
        self.range = []
        for i in range(
            self.cell_y - (self.maze_adapter.height // 4),
            self.cell_y + (self.maze_adapter.height // 4),
        ):
            for j in range(
                self.cell_x - (self.maze_adapter.width // 4),
                self.cell_x + (self.maze_adapter.width // 4),
            ):
                if i < 0 or j < 0:
                    continue
                self.range.append((j, i))


    def movement(self, delta_time):
        pass
        # step = self.speed * self.maze_adapter.cell_size * delta_time
        # dx = self.target_px - self.pixel_x
        # dy = self.target_py - self.pixel_y
        # dist = (dx**2 + dy**2) ** 0.5
        # if dist <= step:
        #     self.cell_x = self.target_cell_x
        #     self.cell_y = self.target_cell_y
        #     self.pixel_x = self.target_px
        #     self.pixel_y = self.target_py
        #     # ########

        #     # ########
        #     self.target_cell_x = self.cell_x + dir_x
        #     self.target_cell_y = self.cell_y + dir_y
        #     self.target_px, self.target_py = self.maze_adapter.cell_to_pixel(
        #         self.target_cell_x, self.target_cell_y
        #     )
        #     self._update_range()
        # else:
        #     self.pixel_x += (dx / dist) * step
        #     self.pixel_y += (dy / dist) * step

    def _shortest_path_next_step(self, start, goal):
        """BFS over the real maze (so it respects actual walls). Returns
        the cell adjacent to `start` to move into next, or None if
        start == goal or no path currently exists."""
        if start == goal:
            return None
        came_from = {start: None}
        frontier = deque([start])
        while frontier:
            current = frontier.popleft()
            if current == goal:
                break
            for neighbor in self.maze_adapter.neighbors(*current):
                if neighbor not in came_from:
                    came_from[neighbor] = current
                    frontier.append(neighbor)
        if goal not in came_from:
            return None
        step = goal
        while came_from[step] != start:
            step = came_from[step]
        return step

    def chase_player(self, delta_time, player):
        step = self.speed * self.maze_adapter.cell_size * delta_time
        dx = self.target_px - self.pixel_x
        dy = self.target_py - self.pixel_y
        dist = (dx**2 + dy**2) ** 0.5
        if dist <= step:
            self.cell_x = self.target_cell_x
            self.cell_y = self.target_cell_y
            self.pixel_x = self.target_px
            self.pixel_y = self.target_py

            next_cell = self._shortest_path_next_step(
                (self.cell_x, self.cell_y), (player.cell_x, player.cell_y)
            )
            if next_cell is None:
                print("YOU LOST")
                sys.exit()

            x, y = next_cell
            dir_x, dir_y = self.get_dir(x, y)
            self.target_cell_x = self.cell_x + dir_x
            self.target_cell_y = self.cell_y + dir_y
            self.target_px, self.target_py = self.maze_adapter.cell_to_pixel(
                self.target_cell_x, self.target_cell_y
            )
            self._update_range()
        else:
            self.pixel_x += (dx / dist) * step
            self.pixel_y += (dy / dist) * step

    def ghosts_running(self):
        pass

    def ghosts_random_move(self, delta_time):
        step = self.speed * self.maze_adapter.cell_size * delta_time
        dx = self.target_px - self.pixel_x
        dy = self.target_py - self.pixel_y
        dist = (dx**2 + dy**2) ** 0.5
        if dist <= step:
            self.cell_x = self.target_cell_x
            self.cell_y = self.target_cell_y
            self.pixel_x = self.target_px
            self.pixel_y = self.target_py
            neighbors = self.maze_adapter.neighbors(self.cell_x, self.cell_y)
            if not neighbors:
                return
            unseen = [n for n in neighbors if n not in self.seen]
            choices = unseen if unseen else neighbors
            x, y = random.choice(choices)
            if len(self.seen) < 3:
                self.seen.append((x, y))
            else:
                self.seen.popleft()
                self.seen.append((x, y))
            dir_x, dir_y = self.get_dir(x, y)
            self.target_cell_x = self.cell_x + dir_x
            self.target_cell_y = self.cell_y + dir_y
            self.target_px, self.target_py = self.maze_adapter.cell_to_pixel(
                self.target_cell_x, self.target_cell_y
            )
            self._update_range()
        else:
            self.pixel_x += (dx / dist) * step
            self.pixel_y += (dy / dist) * step

    def get_dir(self, x, y):
        cor_x = x - self.cell_x
        cor_y = y - self.cell_y
        return cor_x, cor_y

    def update(self, delta_time, player):
        if (player.cell_x, player.cell_y) in self.range:
            self.random_move = False
            self.chase = True
        else:
            self.random_move = True
            self.chase = False
        if self.chase:
            self.chase_player(delta_time, player)
        if self.random_move:
            self.ghosts_random_move(delta_time)


class RedGhost(Ghost):
    pass


class PinkGhost(Ghost):
    pass


class BlueGhost(Ghost):
    pass


class OrangeGhost(Ghost):
    pass