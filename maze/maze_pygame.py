import pygame
from mazegenerator import MazeGenerator
from maze.maze_adapter import MazeAdapter



class Game_loop():
    def __init__(self):
        pygame.init()

        screen = pygame.display.set_mode()
        height = screen.get_height()
        weidth = screen.get_width()

        maze_g = MazeGenerator(size=(30, 15), entry_cell=(0, 0), exit_cell=(15, 15))

        ma = MazeAdapter(maze_g)
        walls = maze_g.maze

        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Background
            screen.fill((0, 0, 0))

            # Draw maze
            for row_index, row in enumerate(walls):
                for col_index, cell_value in enumerate(row):

                    
            pygame.display.flip()

        pygame.quit()

g = Game_loop