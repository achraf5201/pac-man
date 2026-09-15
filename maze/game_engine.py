from maze.maze_entities import Player
import pygame
from mazegenerator import MazeGenerator
from maze.maze_adapter import MazeAdapter
from maze.maze_entities import Player
import math


class Engine:
    def __init__(self, cell_size, score=0, level=1, life=3):
        self.score = score
        self.level = level
        self.life = life
        self.cell_size = cell_size
        self.maze_gen = MazeGenerator(
            size=(34, 18), entry_cell=(0, 0), exit_cell=(15, 15)
        )
        self.maze_adapter = MazeAdapter(self.maze_gen, cell_size)
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.maze_adapter._calc_config(self.screen)

        c_x, c_y = self.maze_adapter.center
        c_px, c_py = self.maze_adapter.cell_to_pixel(c_x, c_y)
        self.player = Player(c_x, c_y, c_px, c_py, 4, self.maze_adapter)

    def eject_player_from_walls(self):
        if self.maze_adapter.walls[self.player.cell_y][self.player.cell_x] == 15:
            neighbors = self.maze_adapter.p_neighbors(
                self.player.cell_x, self.player.cell_y
            )

            for x, y in neighbors:
                if self.maze_adapter.walls[y][x] != 15:
                    px, py = self.maze_adapter.cell_to_pixel(x, y)

                    self.player.cell_x, self.player.cell_y = x, y
                    self.player.pixel_x, self.player.pixel_y = px, py

                    self.player.target_cell_x, self.player.target_cell_y = x, y
                    self.player.target_px, self.player.target_py = px, py

    def _game_loop(self):
        # hadi ghi vibe coditha mafiyach li yfhamha hta nchofo drari kidaro lplayer wndiro b7alhom
        def draw_filled_arc(
            surface, color, center, radius, start_angle_deg, stop_angle_deg
        ):
            """Draws a filled pie-slice/arc on a surface."""
            points = [center]
            for degree in range(start_angle_deg, stop_angle_deg + 1):
                radians = math.radians(degree)

                x = center[0] + radius * math.cos(radians)
                y = center[1] - radius * math.sin(radians)

                points.append((x, y))

            if len(points) > 2:
                pygame.draw.polygon(surface, color, points)

        pygame.init()

        running = True
        clock = pygame.time.Clock()

        self.eject_player_from_walls()
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Background
            self.screen.fill((0, 0, 0))

            # Draw maze
            for row_index, row in enumerate(self.maze_adapter.walls):
                for col_index, cell_value in enumerate(row):
                    pac_px, pac_py = self.maze_adapter.cell_to_pixel(
                        col_index, row_index
                    )
                    if self.maze_adapter.pacgame[row_index][col_index] == 1:
                        pygame.draw.circle(
                            self.screen,
                            (255, 255, 255),
                            (
                                pac_px + self.cell_size // 2,
                                pac_py + self.cell_size // 2,
                            ),
                            self.cell_size // 10,
                        )

                    self.maze_adapter._render_maze(
                        cell_value, col_index, row_index, self.screen
                    )

            keys = pygame.key.get_pressed()

            if keys[pygame.K_w]:
                self.player.next_dir = 1
            elif keys[pygame.K_s]:
                self.player.next_dir = 4

            if keys[pygame.K_a]:
                self.player.next_dir = 8
            elif keys[pygame.K_d]:
                self.player.next_dir = 2
            delta_time = clock.tick(60) / 1000.0
            draw_filled_arc(
                self.screen,
                (255, 0, 0),
                (
                    self.player.pixel_x + self.cell_size // 2,
                    self.player.pixel_y + self.cell_size // 2,
                ),
                (self.cell_size / 2) - self.cell_size // 6,
                int(self.player.start_angle),
                int(self.player.end_angle),
            )
            self.player.update(delta_time, self)
            pygame.display.flip()

        pygame.quit()
