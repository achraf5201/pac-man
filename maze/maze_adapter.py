import sys
import pygame
from maze.maze_model import MazeModel


class MazeAdapter(MazeModel):
    def __init__(self, maze, cell_size=60):
        super().__init__(maze)
        self.screen_width = 0
        self.screen_height = 0
        self.cell_size = cell_size
        self.offset_x = 0
        self.offset_y = 0

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
        self.offset_y = self.screen_height - (self.height * self.cell_size) - self.cell_size // 4

    def _render_hud(self, score=0, lives=3, level=0):
        HUD_HEIGHT = 79
        HUD_WEIGHT = 500
        width = HUD_WEIGHT * 3
        height = (self.height * self.cell_size) + HUD_HEIGHT
        if width >= self.screen_width or height >= self.screen_height:
            print(
                "Error: maze is too large for the current screen "
                "resolution."
            )
            sys.exit(1)
        start_pointx = self.offset_x
        start_pointy = (
            self.offset_y + (self.height * self.cell_size) + HUD_HEIGHT // 10
        )
        self.hud_text.x = start_pointx
        self.hud_text.y = start_pointy
        self.hud_text.text = (
            f"Score: {score}\t\t\t\t\t\t\t\t\t\t\t\t"
            f" Lives: {lives}\t\t\t\t\t\t\t\t\t\t\t\t\t\t"
            f" Level: {level}"
        )
        self.hud_text.draw()

    def _render_maze(self, cell_value, x, y, screen):
        pix, piy = self.cell_to_pixel(x, y)
        if pix + self.cell_size >= self.screen_width or piy + self.cell_size >= self.screen_height:
            print(
                "Error: maze is too large for the current screen "
                "resolution."
            )
            sys.exit(1)
        if cell_value == 15:
            pygame.draw.rect(
                screen,
                (255, 255, 255),
                (pix, piy, self.cell_size, self.cell_size),
            )

        if cell_value & 1:
            pygame.draw.rect(
                screen, (255, 255, 255), (pix, piy, self.cell_size, 2)
            )
        if cell_value & 4:
            pygame.draw.rect(
                screen,
                (255, 255, 255),
                (pix, piy + self.cell_size, self.cell_size, 2),
            )

        if cell_value & 2:
            pygame.draw.rect(
                screen,
                (255, 255, 255),
                (pix + self.cell_size, piy, 2, self.cell_size),
            )

        if cell_value & 8:
            pygame.draw.rect(
                screen, (255, 255, 255), (pix, piy, 2, self.cell_size)
            )
