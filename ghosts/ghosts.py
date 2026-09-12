import arcade
from maze.maze_adapter import MazeAdapter


class ghost(arcade.Sprite):
    def __init__(self, png=None, maze=None, size=0.09):
        super().__init__(png, size)
        self.grid_col = 0
        self.maze_adapter = MazeAdapter(maze)
        self.grid_row = 0
        self.timer = 0
        self.move_interval = 0.3
        self.path = ""
        self.path_index = 0
        self.respawn = False
        self.run = False
        self.chase = False
        self.random_move = True
        self.range = []


class RedGhost(ghost):
    def __init__(self, maze, png="images/red_ghost.png", size=0.09):
        super().__init__(png=png, maze=maze, size=size)


class GreenGhost(ghost):
    def __init__(self, maze, png="images/green_ghost.png", size=0.09):
        super().__init__(png=png, maze=maze, size=size)


class BlueGhost(ghost):
    def __init__(self, maze, png="images/blue_ghost.png", size=0.09):
        super().__init__(png=png, maze=maze, size=size)


class OrangeGhost(ghost):
    def __init__(self, maze, png="images/orange_ghost.png", size=0.09):
        super().__init__(png=png, maze=maze, size=size)


class Ghosts(ghost):
    def __init__(self, maze):
        super().__init__(maze=maze)

        self.red_ghost = RedGhost(maze=maze)
        self.green_ghost = GreenGhost(maze=maze)
        self.blue_ghost = BlueGhost(maze=maze)
        self.orange_ghost = OrangeGhost(maze=maze)

        self.all_sprites = arcade.SpriteList()
        self.all_sprites.append(self.red_ghost)
        self.all_sprites.append(self.green_ghost)
        self.all_sprites.append(self.orange_ghost)
        self.all_sprites.append(self.blue_ghost)
