import pygame
from mazegenerator import MazeGenerator
from maze.maze_adapter import MazeAdapter

pygame.init()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

maze_g = MazeGenerator(size=(38, 21), entry_cell=(0, 0), exit_cell=(15, 15))

cell_size = 50
ma = MazeAdapter(maze_g, cell_size)
ma._calc_config(screen)
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

            ma._render_maze(cell_value, col_index, row_index, screen)
    pygame.display.flip()

pygame.quit()
