import arcade
from mazegenerator import MazeGenerator

maze = MazeGenerator()

HEIGHT_SIZE = len(maze._maze)
WIDTH_SIZE = len(maze._maze[0])
print(HEIGHT_SIZE)
print(WIDTH_SIZE)
CELL_SIZE = 40


class MazeView(arcade.View):

    def on_draw(self):
        self.clear()
        for row_index, row in enumerate(maze._maze):
            for col_index, cell_value in enumerate(row):
                x = col_index * CELL_SIZE
                y = (HEIGHT_SIZE - 1 - row_index) * CELL_SIZE

                if cell_value & 1:
                    arcade.draw_lbwh_rectangle_filled(
                        x, y + CELL_SIZE - 5, CELL_SIZE, 5, arcade.color.BLUE
                    )

                if cell_value & 2:
                    arcade.draw_lbwh_rectangle_filled(
                        x + CELL_SIZE - 5, y, 5, CELL_SIZE, arcade.color.BLUE
                    )

                if cell_value & 4:
                    arcade.draw_lbwh_rectangle_filled(
                        x, y, CELL_SIZE, 5, arcade.color.BLUE
                    )

                if cell_value & 8:
                    arcade.draw_lbwh_rectangle_filled(
                        x, y, 5, CELL_SIZE, arcade.color.BLUE
                    )


window = arcade.Window(fullscreen=True, title="Maze")

view = MazeView()
window.show_view(view)

arcade.run()
