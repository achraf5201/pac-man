from mazegenerator import MazeGenerator
import arcade

maze = MazeGenerator()

print(maze._perfect)


def draw_maze(maze):

    rows = len(maze)
    cols = len(maze[0])

    horizontal = "---"

    print(
        "+"
        + "+".join(
            horizontal if maze[0][c] & 1 else "   " for c in range(cols)
        )
        + "+"
    )
    for r in range(rows):
        line = ""
        for c in range(cols):
            if maze[r][c] & 8:
                line += "|"
            else:
                line += " "
            line += "   "
        if maze[r][cols - 1] & 2:
            line += "|"
        else:
            line += " "
        print(line)
        line = "+"
        for c in range(cols):
            if maze[r][c] & 4:
                line += "---"
            else:
                line += "   "

            if c < cols - 1:
                line += "+"
        line += "+"
        print(line)


if not maze._perfect:
    draw_maze(maze._maze)


class Gosts:
    def random_movement():
        pass

    def chasing():
        pass

    def fleeing():
        pass

    def respawn():
        pass


class player:
    pass


class Pac_Man:
    def __init__(self):
        self.highscore_filename = ""
        self.level
        self.width
        self.lives
        self.pacgum
        self.points_per_pacgum
        self.points_per_super_pacgum
        self.points_per_ghost
        self.seed
        self.level_max_time

import arcade

WIDTH = 800
HEIGHT = 600


class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(WIDTH, HEIGHT, "Moving Player")

        self.player_x = 400
        self.player_y = 300
        self.speed = 20

    def on_draw(self):
        self.clear()
        arcade.draw_circle_filled(
            self.player_x,
            self.player_y,
            25,
            arcade.color.BLUE
        )

    def on_key_press(self, key, modifiers):
        if key == arcade.key.LEFT:
            self.player_x -= self.speed
        elif key == arcade.key.RIGHT:
            self.player_x += self.speed
        elif key == arcade.key.UP:
            self.player_y += self.speed
        elif key == arcade.key.DOWN:
            self.player_y -= self.speed


game = MyGame()
arcade.run()