# from maze.maze_view import GameView
# import arcade


# def main():
#     window = arcade.Window(fullscreen=True, title="Maze")

#     view = GameView()
#     window.show_view(view)
#     arcade.run()


# if __name__ == "__main__":
#     main()
import pygame
from maze.maze_adapter import MazeAdapter
from mazegenerator import MazeGenerator

pygame.init()

screen = pygame.display.set_mode((800, 600))

red = (255, 0, 0)
maze_g = MazeGenerator(size=(38, 20), entry_cell=(0, 0), exit_cell=(15, 15))
adapter = MazeAdapter(maze_g, 40)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    for row_index, row in enumerate(adapter.walls):
        for col_index, cell_value in enumerate(row):
            x, y = adapter.cell_to_pixel(col_index, row_index)
            print(x, y)
            adapter._render_maze(cell_value, x, y, screen)


    screen.fill((0, 0, 0))

    pygame.display.flip()

pygame.quit()
