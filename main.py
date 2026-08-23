import arcade
from mazegenerator import MazeGenerator

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


    def _calc_config(self):
        self.maze_width = len(self.maze._maze[0])
        self.maze_height = len(self.maze._maze)
        self.screen_width, self.screen_height = arcade.get_display_size()
        self.cell_size = 70

        self.offset_x = (self.screen_width - self.maze_width * self.cell_size) / 2
        self.offset_y = (self.screen_height - self.maze_height * self.cell_size) / 2


    def on_draw(self):
        self.clear()
        for row_index, row in enumerate(self.maze._maze):
            for col_index, cell_value in enumerate(row):
                x = self.offset_x + col_index * self.cell_size
                y = self.offset_y + (self.maze_height - 1 - row_index) * self.cell_size

                if cell_value == 15:
                    arcade.draw_lbwh_rectangle_filled(
                        x, y, self.cell_size, self.cell_size, arcade.color.WHITE
                    )

                if cell_value & 1:
                    arcade.draw_lbwh_rectangle_filled(
                        x, y + self.cell_size, self.cell_size, 2, arcade.color.WHITE
                    )

                if cell_value & 2:
                    arcade.draw_lbwh_rectangle_filled(
                        x + self.cell_size, y, 2, self.cell_size, arcade.color.WHITE
                    )

                if cell_value & 4:
                    arcade.draw_lbwh_rectangle_filled(
                        x, y, self.cell_size, 2, arcade.color.WHITE
                    )

                if cell_value & 8:
                    arcade.draw_lbwh_rectangle_filled(
                        x, y, 2, self.cell_size, arcade.color.WHITE
                    )


def main():
    maze = MazeGenerator()
    window = arcade.Window(fullscreen=True, title="Maze")

    view = MazeView(maze)
    window.show_view(view)
    arcade.run()

if __name__ == "__main__":
    main()
