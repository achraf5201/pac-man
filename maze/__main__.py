import pygame
from mazegenerator import MazeGenerator
from maze.maze_adapter import MazeAdapter
from maze.maze_entities import Player
import math


# hadi ghi vibe coditha mafiyach li yfhamha hta nchofo drari kidaro lplayer wndiro b7alhom
def draw_filled_arc(surface, color, center, radius, start_angle_deg, stop_angle_deg):
    """Draws a filled pie-slice/arc on a surface."""
    points = [center]
    for degree in range(start_angle_deg, stop_angle_deg + 1):
        radians = math.radians(degree)

        x = center[0] + radius * math.cos(radians)
        y = center[1] - radius * math.sin(radians)

        points.append((x, y))

    if len(points) > 2:
        pygame.draw.polygon(surface, color, points)


pygame.init()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

maze_g = MazeGenerator(size=(27, 14), entry_cell=(0, 0), exit_cell=(15, 15))


cell_size = 50
ma = MazeAdapter(maze_g, cell_size)
ma._calc_config(screen)

walls = maze_g.maze

running = True
clock = pygame.time.Clock()


c_x, c_y = ma.center
c_px, c_py = ma.cell_to_pixel(c_x, c_y)
player = Player(c_x, c_y, c_px, c_py, 4, ma)


def eject_player_from_walls():
    if ma.walls[player.cell_y][player.cell_x] == 15:
        neighbors = ma.p_neighbors(player.cell_x, player.cell_y)

        for x, y in neighbors:
            if ma.walls[y][x] != 15:
                px, py = ma.cell_to_pixel(x, y)

                player.cell_x, player.cell_y = x, y
                player.pixel_x, player.pixel_y = px, py

                player.target_cell_x, player.target_cell_y = x, y
                player.target_px, player.target_py = px, py


eject_player_from_walls()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Background
    screen.fill((0, 0, 0))

    # Draw maze
    for row_index, row in enumerate(walls):
        for col_index, cell_value in enumerate(row):
            pac_px, pac_py = ma.cell_to_pixel(col_index, row_index)
            if ma.pacgame[row_index][col_index] == 1:
                draw_filled_arc(
                    screen,
                    (255, 255, 255),
                    (pac_px + cell_size // 2, pac_py + cell_size // 2),
                    cell_size // 10,
                    0, 360
                )

            ma._render_maze(cell_value, col_index, row_index, screen)

    keys = pygame.key.get_pressed()

    if keys[pygame.K_w]:
        player.next_dir = 1
    elif keys[pygame.K_s]:
        player.next_dir = 4

    if keys[pygame.K_a]:
        player.next_dir = 8
    elif keys[pygame.K_d]:
        player.next_dir = 2
    delta_time = clock.tick(60) / 1000.0
    draw_filled_arc(
        screen,
        (255, 0, 0),
        (player.pixel_x + cell_size // 2, player.pixel_y + cell_size // 2),
        (cell_size / 2) - cell_size // 6,
        int(player.start_angle),
        int(player.end_angle),
    )
    player.update(delta_time)

    pygame.display.flip()

pygame.quit()
