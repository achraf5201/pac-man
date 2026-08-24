import arcade
import random
from mazegenerator import MazeGenerator


class RedGhost(arcade.Sprite):
    def __init__(self, filename):
        super().__init__(filename, 0.09)
        self._speedx = 100
        self._speedy = 100
        self.grid_col = 0
        self.grid_row = 0
        self.timer = 0


class GreenGhost(arcade.Sprite):
    def __init__(self, filename):
        super().__init__(filename, 0.09)


class BlueGhost(arcade.Sprite):
    def __init__(self, filename):
        super().__init__(filename, 0.09)


class OrangeGhost(arcade.Sprite):
    def __init__(self, filename):
        super().__init__(filename, 0.09)


class MazeView(arcade.View):

    def __init__(self, maze):
        super().__init__()
        self.maze = maze
        self.maze_width = 0
        self.maze_height = 0
        self.screen_width = 0
        self.screen_height = 0
        self.cell_size = 0
        self.offset_x = 0
        self.offset_y = 0

        self._calc_config()

        self.all_sprites = arcade.SpriteList()

        self.red_ghost = RedGhost("images/red_ghost.png")
        self.red_ghost.center_x = self.offset_x + self.cell_size / 2
        self.red_ghost.center_y = (
            self.offset_y
            + (self.maze_height - 1) * self.cell_size
            + self.cell_size / 2
        )
        print(self.red_ghost.center_x, self.offset_x, self.cell_size)
        print(self.red_ghost.center_y, self.offset_y, self.cell_size)

        self.green_ghost = GreenGhost("images/green_ghost.png")
        self.green_ghost.center_x = self.offset_x + self.cell_size / 2
        self.green_ghost.center_y = self.offset_y + self.cell_size / 2

        self.orange_ghost = OrangeGhost("images/orange_ghost.png")
        self.orange_ghost.center_x = (
            self.offset_x
            + ((len(self.maze._maze[0]) - 1) * self.cell_size)
            + self.cell_size / 2
        )
        self.orange_ghost.center_y = self.offset_y + self.cell_size / 2

        self.blue_ghost = BlueGhost("images/blue_ghost.png")
        self.blue_ghost.center_x = (
            self.offset_x
            + ((len(self.maze._maze[0]) - 1) * self.cell_size)
            + self.cell_size / 2
        )
        self.blue_ghost.center_y = (
            self.offset_y
            + ((len(self.maze._maze) - 1) * self.cell_size)
            + self.cell_size / 2
        )

        self.all_sprites.append(self.red_ghost)
        self.all_sprites.append(self.green_ghost)
        self.all_sprites.append(self.orange_ghost)
        self.all_sprites.append(self.blue_ghost)
        self.ra = 0

    def _calc_config(self):
        self.maze_width = len(self.maze._maze[0])
        self.maze_height = len(self.maze._maze)
        self.screen_width, self.screen_height = arcade.get_display_size()
        self.cell_size = 70

        self.offset_x = (
            self.screen_width - self.maze_width * self.cell_size
        ) / 2
        self.offset_y = (
            self.screen_height - self.maze_height * self.cell_size
        ) / 2

    def on_draw(self):
        self.clear()
        for row_index, row in enumerate(self.maze._maze):
            for col_index, cell_value in enumerate(row):
                x = self.offset_x + col_index * self.cell_size
                y = (
                    self.offset_y
                    + (self.maze_height - 1 - row_index) * self.cell_size
                )

                if cell_value == 15:
                    arcade.draw_lbwh_rectangle_filled(
                        x,
                        y,
                        self.cell_size,
                        self.cell_size,
                        arcade.color.WHITE,
                    )

                if cell_value & 1:
                    arcade.draw_lbwh_rectangle_filled(
                        x,
                        y + self.cell_size,
                        self.cell_size,
                        2,
                        arcade.color.WHITE,
                    )

                if cell_value & 2:
                    arcade.draw_lbwh_rectangle_filled(
                        x + self.cell_size,
                        y,
                        2,
                        self.cell_size,
                        arcade.color.WHITE,
                    )

                if cell_value & 4:
                    arcade.draw_lbwh_rectangle_filled(
                        x, y, self.cell_size, 2, arcade.color.WHITE
                    )

                if cell_value & 8:
                    arcade.draw_lbwh_rectangle_filled(
                        x, y, 2, self.cell_size, arcade.color.WHITE
                    )

        self.all_sprites.draw()

    def on_update(self, delta_time):

        self.red_ghost.timer += delta_time
        if self.red_ghost.timer >= 0.6915:
            self.red_ghost.timer = 0
            self.ra = random.choice([0, 1])
        if self.ra == 0:
            self.red_ghost.center_x += self.red_ghost._speedx * delta_time
        else:
            self.red_ghost.center_y += self.red_ghost._speedy * delta_time
        if self.red_ghost.center_x > (self.offset_x + ((len(self.maze._maze[0]) - 1) * self.cell_size) + self.cell_size / 2):
            self.red_ghost.center_x = (self.offset_x + ((len(self.maze._maze[0]) - 1) * self.cell_size) + self.cell_size / 2)
            self.red_ghost._speedx *= -1
        if self.red_ghost.center_y > (self.offset_y + ((len(self.maze._maze) - 1) * self.cell_size) + self.cell_size / 2):
            self.red_ghost.center_y = (self.offset_y + ((len(self.maze._maze) - 1) * self.cell_size) + self.cell_size / 2)
            self.red_ghost._speedy *= -1
        if self.red_ghost.center_x < self.offset_x + self.cell_size / 2:
            self.red_ghost.center_x = self.offset_x + self.cell_size / 2
            self.red_ghost._speedx *= -1
        if self.red_ghost.center_y < self.offset_y + self.cell_size / 2:
            self.red_ghost.center_y = self.offset_y + self.cell_size / 2
            self.red_ghost._speedy *= -1


def main():
    maze = MazeGenerator(entry_cell=(0, 0), exit_cell=(15, 15))
    window = arcade.Window(fullscreen=True, title="Maze")

    view = MazeView(maze)
    window.show_view(view)
    arcade.run()


if __name__ == "__main__":
    main()
