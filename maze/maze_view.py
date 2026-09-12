import arcade
from maze.maze_adapter import MazeAdapter
from mazegenerator import MazeGenerator
from maze.maze_entities import Player


class GameView(arcade.View):
    def __init__(self, cell_size=50):
        super().__init__()
        self.maze_g = MazeGenerator(
            size=(38, 20), entry_cell=(0, 0), exit_cell=(15, 15)
        )
        self.maze_adapter = MazeAdapter(self.maze_g, cell_size)
        self.maze_adapter._calc_config()
        self.cell_size = cell_size

        c_x, c_y = self.maze_adapter.center
        p_x, p_y = self.maze_adapter.cell_to_pixel(c_x, c_y)

        self.player = Player(c_x, c_y, p_x, p_y, 3, self.maze_adapter)
        self._eject_player_from_walls()

    def _eject_player_from_walls(self):
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

    def on_draw(self):
        self.clear()

        for row_index, row in enumerate(self.maze_adapter.walls):
            for col_index, cell_value in enumerate(row):
                x, y = self.maze_adapter.cell_to_pixel(col_index, row_index)
                self.maze_adapter._render_maze(cell_value, x, y)

        self.maze_adapter._render_hud()

        arcade.draw_arc_filled(
            self.player.pixel_x + self.cell_size / 2,
            self.player.pixel_y + self.cell_size / 2,
            self.cell_size - self.cell_size // 4,
            self.cell_size - self.cell_size // 4,
            arcade.color.RED,
            self.player.start_angle,
            self.player.end_angle,
        )

    def on_update(self, delta_time):
        self.player.update(delta_time)

    def on_key_press(self, symbol, modifiers):
        if symbol in (arcade.key.UP, arcade.key.W):
            self.player.next_dir = 1
        elif symbol in (arcade.key.RIGHT, arcade.key.D):
            self.player.next_dir = 2
        elif symbol in (arcade.key.DOWN, arcade.key.S):
            self.player.next_dir = 4
        elif symbol in (arcade.key.LEFT, arcade.key.A):
            self.player.next_dir = 8
