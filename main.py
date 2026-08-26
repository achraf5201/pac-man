import arcade
import random
from mazegenerator import MazeGenerator


class RedGhost(arcade.Sprite):
    def __init__(self, filename, size=0.09):
        super().__init__(filename, size)
        self.grid_col = 0
        self.grid_row = 0
        self.timer = 0
        self.move_interval = 0.3
        self.path = ""
        self.path_index = 0


class GreenGhost(arcade.Sprite):
    def __init__(self, filename, size=0.09):
        super().__init__(filename, size)


class BlueGhost(arcade.Sprite):
    def __init__(self, filename, size=0.09):
        super().__init__(filename, size)


class OrangeGhost(arcade.Sprite):
    def __init__(self, filename, size=0.09):
        super().__init__(filename, size)


class MazeView(arcade.View):

    def __init__(self, maze, cell_size=50):
        super().__init__()
        self.maze = maze
        self.maze_width = 0
        self.maze_height = 0
        self.screen_width = 0
        self.screen_height = 0
        self.cell_size = cell_size
        self.offset_x = 0
        self.offset_y = 0

        self._calc_config()

        self.all_sprites = arcade.SpriteList()
        self.red_ghost = RedGhost(
            "images/red_ghost.png", size=(cell_size / 700)
        )
        self.red_ghost.grid_col = 0
        self.red_ghost.grid_row = 0
        self.red_ghost.center_x = self.offset_x + self.cell_size / 2
        self.red_ghost.center_y = (
            self.offset_y
            + (self.maze_height - 1) * self.cell_size
            + self.cell_size / 2
        )
        self.red_ghost.path = self.maze._shortest_path

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

        self.offset_x = (
            self.screen_width - self.maze_width * self.cell_size
        ) / 2
        self.offset_y = (
            self.screen_height - self.maze_height * self.cell_size
        ) / 2

    def grid_to_pixel(self, row, col):
        x = self.offset_x + col * self.cell_size + self.cell_size / 2
        y = (
            self.offset_y
            + (self.maze_height - 1 - row) * self.cell_size
            + self.cell_size / 2
        )
        return x, y

    def get_open_directions(self, index):
        if index >= len(self.red_ghost.path):
            return None

        direction = self.red_ghost.path[index]

        if direction == "S":
            return (0, 1)
        elif direction == "N":
            return (0, -1)
        elif direction == "E":
            return (1, 0)
        elif direction == "W":
            return (-1, 0)

        return None

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

    def _red_ghost_move(self, delta_time):

        if not hasattr(self.red_ghost, "start_y"):
            self.red_ghost.target_x = self.red_ghost.center_x
            self.red_ghost.target_y = self.red_ghost.center_y
            self.red_ghost.start_x = self.red_ghost.center_x
            self.red_ghost.start_y = self.red_ghost.center_y

        self.red_ghost.timer += delta_time

        if self.red_ghost.timer < self.red_ghost.move_interval:
            progress = self.red_ghost.timer / self.red_ghost.move_interval
            print(progress)
            self.red_ghost.center_x = (
                self.red_ghost.start_x
                + (self.red_ghost.target_x - self.red_ghost.start_x) * progress
            )
            self.red_ghost.center_y = (
                self.red_ghost.start_y
                + (self.red_ghost.target_y - self.red_ghost.start_y) * progress
            )
            print(self.red_ghost.center_x, self.red_ghost.center_y)

        else:
            self.red_ghost.center_x = self.red_ghost.target_x
            self.red_ghost.center_y = self.red_ghost.target_y
            print(self.red_ghost.center_x, self.red_ghost.center_y)

            options = self.get_open_directions(
                self.red_ghost.path_index,
            )
            if options:
                col, row = options
                self.red_ghost.path_index += 1
                self.red_ghost.grid_row += row
                self.red_ghost.grid_col += col

                self.red_ghost.start_x = self.red_ghost.center_x
                self.red_ghost.start_y = self.red_ghost.center_y

                self.red_ghost.target_x, self.red_ghost.target_y = (
                    self.grid_to_pixel(
                        self.red_ghost.grid_row, self.red_ghost.grid_col
                    )
                )

                self.red_ghost.timer -= self.red_ghost.move_interval
            else:
                self.red_ghost.timer = self.red_ghost.move_interval

    def on_update(self, delta_time):
        self._red_ghost_move(delta_time)


def main():
    maze = MazeGenerator(size=(27, 15), entry_cell=(0, 0), exit_cell=(15, 15))
    window = arcade.Window(fullscreen=True, title="Maze")

    view = MazeView(maze, cell_size=60)
    window.show_view(view)
    arcade.run()


if __name__ == "__main__":
    main()
