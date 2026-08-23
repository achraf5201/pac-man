import arcade
from mazegenerator import MazeGenerator

maze = MazeGenerator()

HEIGHT_SIZE = len(maze._maze)
WIDTH_SIZE = len(maze._maze[0])
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
CELL_SIZE = 40

offset_x = (SCREEN_WIDTH - WIDTH_SIZE * CELL_SIZE) / 2
offset_y = (SCREEN_HEIGHT - HEIGHT_SIZE * CELL_SIZE) / 2


class MazeView(arcade.View):

    def on_draw(self):
        self.clear()
        for row_index, row in enumerate(maze._maze):
            for col_index, cell_value in enumerate(row):
                x = offset_x + col_index * CELL_SIZE
                y = offset_y + (HEIGHT_SIZE - 1 - row_index) * CELL_SIZE

                if cell_value == 15:
                    arcade.draw_lbwh_rectangle_filled(
                        x, y, CELL_SIZE, CELL_SIZE, arcade.color.WHITE
                    )

                if cell_value & 1:
                    arcade.draw_lbwh_rectangle_filled(
                        x, y + CELL_SIZE, CELL_SIZE, 2, arcade.color.WHITE
                    )

                if cell_value & 2:
                    arcade.draw_lbwh_rectangle_filled(
                        x + CELL_SIZE, y, 2, CELL_SIZE, arcade.color.WHITE
                    )

                if cell_value & 4:
                    arcade.draw_lbwh_rectangle_filled(
                        x, y, CELL_SIZE, 2, arcade.color.WHITE
                    )

                if cell_value & 8:
                    arcade.draw_lbwh_rectangle_filled(
                        x, y, 2, CELL_SIZE, arcade.color.WHITE
                    )


window = arcade.Window(fullscreen=True, title="Maze")

view = MazeView()
window.show_view(view)

arcade.run()
