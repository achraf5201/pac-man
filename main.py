import arcade
import random
from mazegenerator import MazeGenerator


class RedGhost(arcade.Sprite):
    def __init__(self, filename):
        super().__init__(filename, 0.09)
        self.grid_col = 0
        self.grid_row = 0
        self.timer = 0
        self.move_interval = 0.3


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
        self.red_ghost.grid_col = 0
        self.red_ghost.grid_row = 0
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
    
    def grid_to_pixel(self, col, row): #katconverti grid coordinates l pixel to show it on the viusalizer
        x = self.offset_x + col * self.cell_size + self.cell_size / 2  # self.offset_x useless space + col = 3 so we need to skip three cols andrboha b cell_size o kanzid another col / 2 to land in the middle
        y = (
            self.offset_y
            + (self.maze_height - 1 - row) * self.cell_size # maze_height => example 16 - 1 bcs of len() [[row1],[row2], [row3]] 
            + self.cell_size / 2 # same logic
        )
        return x, y

    def get_open_directions(self, col, row):
        cell_value = self.maze._maze[row][col]
        directions = []
        if not cell_value & 1:
            directions.append((0, -1))
        if not cell_value & 2:
            directions.append((1, 0))
        if not cell_value & 4:
            directions.append((0, 1))
        if not cell_value & 8:
            directions.append((-1, 0))
        return directions

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
        ghost = self.red_ghost
        ghost.timer += delta_time

        if ghost.timer >= ghost.move_interval:
            ghost.timer = 0

            options = self.get_open_directions(ghost.grid_col, ghost.grid_row)
            if options:
                dcol, drow = random.choice(options)
                ghost.grid_col += dcol
                ghost.grid_row += drow

                x, y = self.grid_to_pixel(ghost.grid_col, ghost.grid_row)
                ghost.center_x = x
                ghost.center_y = y


def main():
    maze = MazeGenerator(entry_cell=(0, 0), exit_cell=(15, 15))
    window = arcade.Window(fullscreen=True, title="Maze")

    view = MazeView(maze)
    window.show_view(view)
    arcade.run()


if __name__ == "__main__":
    main()
