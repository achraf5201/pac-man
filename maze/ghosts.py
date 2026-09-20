import random
from collections import deque
import sys
import pygame


class Ghost:
    def __init__(self, x, y, pixel_x, pixel_y, speed, maze_adapter):
        self.cell_x = x
        self.cell_y = y
        self.source_x = x
        self.source_y = y
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
        self.ghost_dead = False

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

    def _shortest_path_next_step(self, start, goal):
        if start == goal:
            return None
        d = {start: None}
        queue = deque([start])
        while queue:
            x, y = queue.popleft()
            if (x, y) == goal:
                break
            for neighbor in self.maze_adapter.neighbors(x, y):
                if neighbor not in d:
                    d[neighbor] = (x, y)
                    queue.append(neighbor)
        if goal not in d:
            return None
        step = goal
        while d[step] != start:
            step = d[step]
        return step

    def _shortest_path(self, start, goal):
        if start == goal:
            return None

        d = {start: None}
        queue = deque([start])

        while queue:
            current = queue.popleft()

            if current == goal:
                break

            for neighbor in self.maze_adapter.neighbors(*current):
                if neighbor not in d:
                    d[neighbor] = current
                    queue.append(neighbor)

        if goal not in d:
            return None

        path = []
        current = goal

        while current is not None:
            path.append(current)
            current = d[current]

        path.reverse()
        return path

    def chase_player(self, delta_time, player):
        if player.cell_x == self.cell_x and player.cell_y == self.cell_y:
            print("YOU LOST")
            sys.exit()
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

    def dead(self, delta_time):
        step = 10 * self.maze_adapter.cell_size * delta_time

        dx = self.target_px - self.pixel_x
        dy = self.target_py - self.pixel_y
        dist = (dx**2 + dy**2) ** 0.5

        if dist <= step:
            self.cell_x = self.target_cell_x
            self.cell_y = self.target_cell_y
            self.pixel_x = self.target_px
            self.pixel_y = self.target_py

            next_cell = self._shortest_path_next_step(
                (self.cell_x, self.cell_y), (self.source_x, self.source_y)
            )
            if next_cell is None:
                self.ghost_dead = False
                return
            x, y = next_cell
            dir_x, dir_y = self.get_dir(x, y)

            self.target_cell_x = self.cell_x + dir_x
            self.target_cell_y = self.cell_y + dir_y

            self.target_px, self.target_py = self.maze_adapter.cell_to_pixel(
                self.target_cell_x, self.target_cell_y
            )
        else:
            self.pixel_x += (dx / dist) * step
            self.pixel_y += (dy / dist) * step

    def ghosts_running(self, delta_time, player):
        if player.cell_x == self.cell_x and player.cell_y == self.cell_y:
            self.ghost_dead = True
            self.dead_mode()

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
        if (player.cell_x, player.cell_y) in self.range and not self.run:
            self.random_move = False
            self.chase = True
        elif self.run:
            self.random_move = False
            self.chase = False
        elif self.ghost_dead:
            self.random_move = False
            self.chase = False
            self.run = False
        else:
            self.random_move = True
            self.chase = False

        if self.chase:
            self.chase_player(delta_time, player)
        if self.random_move:
            self.ghosts_random_move(delta_time)
        if self.run:
            self.ghosts_running(delta_time, player)
        if self.ghost_dead:
            self.dead(delta_time)

    def scare_mode(self):
        self.sprite = pygame.image.load("assets/ghost_images/powerup.png")
        self.sprite = pygame.transform.scale(
            self.sprite,
            (
                self.maze_adapter.cell_size - self.maze_adapter.cell_size // 4,
                self.maze_adapter.cell_size - self.maze_adapter.cell_size // 4,
            ),
        )
        self.run = True
        self.random_move = False

    def normal_mode(self, png):
        self.sprite = pygame.image.load(png)
        self.sprite = pygame.transform.scale(
            self.sprite,
            (
                self.maze_adapter.cell_size - self.maze_adapter.cell_size // 4,
                self.maze_adapter.cell_size - self.maze_adapter.cell_size // 4,
            ),
        )
        self.run = False
        self.random_move = True

    def dead_mode(self):
        self.sprite = pygame.image.load("assets/ghost_images/dead.png")
        self.sprite = pygame.transform.scale(
            self.sprite,
            (
                self.maze_adapter.cell_size - self.maze_adapter.cell_size // 4,
                self.maze_adapter.cell_size - self.maze_adapter.cell_size // 4,
            ),
        )


class RedGhost(Ghost):
    def __init__(self, x, y, pixel_x, pixel_y, speed, maze_adapter):
        super().__init__(x, y, pixel_x, pixel_y, speed, maze_adapter)
        self.sprite = pygame.image.load("assets/ghost_images/red.png")
        self.sprite = pygame.transform.scale(
            self.sprite,
            (
                self.maze_adapter.cell_size - self.maze_adapter.cell_size // 4,
                self.maze_adapter.cell_size - self.maze_adapter.cell_size // 4,
            ),
        )


class PinkGhost(Ghost):
    def __init__(self, x, y, pixel_x, pixel_y, speed, maze_adapter):
        super().__init__(x, y, pixel_x, pixel_y, speed, maze_adapter)
        self.sprite = pygame.image.load("assets/ghost_images/pink.png")
        self.sprite = pygame.transform.scale(
            self.sprite,
            (
                self.maze_adapter.cell_size - self.maze_adapter.cell_size // 4,
                self.maze_adapter.cell_size - self.maze_adapter.cell_size // 4,
            ),
        )


class BlueGhost(Ghost):
    def __init__(self, x, y, pixel_x, pixel_y, speed, maze_adapter):
        super().__init__(x, y, pixel_x, pixel_y, speed, maze_adapter)
        self.sprite = pygame.image.load("assets/ghost_images/blue.png")
        self.sprite = pygame.transform.scale(
            self.sprite,
            (
                self.maze_adapter.cell_size - self.maze_adapter.cell_size // 4,
                self.maze_adapter.cell_size - self.maze_adapter.cell_size // 4,
            ),
        )


class OrangeGhost(Ghost):
    def __init__(self, x, y, pixel_x, pixel_y, speed, maze_adapter):
        super().__init__(x, y, pixel_x, pixel_y, speed, maze_adapter)
        self.sprite = pygame.image.load("assets/ghost_images/orange.png")
        self.sprite = pygame.transform.scale(
            self.sprite,
            (
                self.maze_adapter.cell_size - self.maze_adapter.cell_size // 4,
                self.maze_adapter.cell_size - self.maze_adapter.cell_size // 4,
            ),
        )
