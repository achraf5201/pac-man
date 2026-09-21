import sys
import pygame
from maze.maze_model import MazeModel


class MazeAdapter(MazeModel):
    def __init__(self, maze, cell_size):
        super().__init__(maze)
        self.screen_width = 0
        self.screen_height = 0
        self.cell_size = cell_size
        self.offset_x = 0
        self.offset_y = 0
        
        pygame.font.init()
        self.font = pygame.font.SysFont(None, 36)

        self.pacgum = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                if (
                    (i == 0 and j == 0)
                    or (i == 0 and j == self.width - 1)
                    or (i == self.height - 1 and j == 0)
                    or (i == self.height - 1 and j == self.width - 1)
                ) or self.walls[i][j] == 15:
                    row.append(0)
                else:
                    row.append(1)
            self.pacgum.append(row)
            
        self.super_pacgum = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                if (
                    (i == 0 and j == 0)
                    or (i == 0 and j == self.width - 1)
                    or (i == self.height - 1 and j == 0)
                    or (i == self.height - 1 and j == self.width - 1)
                ):
                    row.append(1)
                else:
                    row.append(0)
            self.super_pacgum.append(row)

    def cell_to_pixel(self, x, y):
        pix_x = self.offset_x + (x * self.cell_size)
        pix_y = self.offset_y + (y * self.cell_size)
        return pix_x, pix_y

    def pixel_to_cell(self, pix_x, pix_y):
        x = (pix_x - self.offset_x) // self.cell_size
        y = (pix_y - self.offset_y) // self.cell_size
        return x, y

    def _calc_config(self, screen):

        width = self.width * self.cell_size
        height = self.height * self.cell_size
        self.screen_width, self.screen_height = screen.get_size()
        if width >= self.screen_width or height >= self.screen_height:
            print(
                "Error: maze is too large for the current screen "
                "resolution."
            )
            sys.exit(1)

        self.offset_x = (
            self.screen_width - (self.width * self.cell_size)
        ) // 2
        self.offset_y = (
            self.screen_height - (self.height * self.cell_size)
        ) // 2

    def _render_hud(self, screen, score=0, lives=3, level=0):
        if not hasattr(self, 'font'):
            pygame.font.init()
            self.font = pygame.font.SysFont(None, 36)

        start_pointx = self.offset_x
        start_pointy = self.offset_y - 40 
        
        hud_string = f"Score: {score}          Lives: {lives}          Level: {level}"
        text_surface = self.font.render(hud_string, True, (255, 255, 255))
        
        screen.blit(text_surface, (start_pointx, start_pointy))

    def _render_maze(self, cell_value, x, y, screen):
        pix, piy = self.cell_to_pixel(x, y)
        if (
            pix + self.cell_size >= self.screen_width
            or piy + self.cell_size >= self.screen_height
        ):
            print(
                "Error: maze is too large for the current screen "
                "resolution."
            )
            sys.exit(1)
            
        if cell_value == 15:
            pygame.draw.rect(
                screen,
                'blue',
                (pix, piy, self.cell_size, self.cell_size),
            )

        if cell_value & 1:
            pygame.draw.rect(screen, "blue", (pix, piy, self.cell_size, 4))
        if cell_value & 4:
            pygame.draw.rect(
                screen,
                "blue",
                (pix, piy + self.cell_size, self.cell_size, 4),
            )

        if cell_value & 2:
            pygame.draw.rect(
                screen,
                "blue",
                (pix + self.cell_size, piy, 4, self.cell_size),
            )

        if cell_value & 8:
            pygame.draw.rect(screen, "blue", (pix, piy, 4, self.cell_size))

        center_x = pix + (self.cell_size // 2)
        center_y = piy + (self.cell_size // 2)

        if self.pacgum[y][x] == 1:
            pygame.draw.circle(screen, (255, 255, 255), (center_x, center_y), 4)
        elif self.super_pacgum[y][x] == 1:
            pygame.draw.circle(screen, (255, 255, 255), (center_x, center_y), 10)