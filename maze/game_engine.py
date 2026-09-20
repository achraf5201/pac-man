import pygame
from mazegenerator import MazeGenerator
from maze.maze_adapter import MazeAdapter
from maze.player import Player
from maze.ghosts import RedGhost, PinkGhost, BlueGhost, OrangeGhost
import math
from enum import Enum
import time


# hadi an7aydoha w andiro tssawer yloopi 3lihom
def draw_filled_arc(
    surface, color, center, radius, start_angle_deg, stop_angle_deg
):
    """Draws a filled pie-slice/arc on a surface."""
    points = [center]
    for degree in range(start_angle_deg, stop_angle_deg + 1):
        radians = math.radians(degree)

        x = center[0] + radius * math.cos(radians)
        y = center[1] - radius * math.sin(radians)

        points.append((x, y))

    if len(points) > 2:
        pygame.draw.polygon(surface, color, points)


class GameState(Enum):
    MAIN_MENU = 1
    CREDITS = 2
    SETTINGS = 3
    HIGHSCORES = 4

    PLAYING = 5
    PAUSE = 6
    GAME_OVER = 7
    VICTORY = 8


class Engine:
    def __init__(self, cell_size, score=0, level=1, life=3):
        pygame.init()

        self.score = score
        self.super_power = False
        self.start_time = 0
        self.end_time = 0
        self.level = level
        self.life = life
        self.cell_size = cell_size
        self.maze_gen = MazeGenerator(
            size=(15, 15), entry_cell=(0, 0), exit_cell=(15, 15)
        )
        self.maze_adapter = MazeAdapter(self.maze_gen, cell_size)
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.maze_adapter._calc_config(self.screen)

        c_x, c_y = self.maze_adapter.center
        c_px, c_py = self.maze_adapter.cell_to_pixel(c_x, c_y)
        self.player = Player(c_x, c_y, c_px, c_py, 4, self.maze_adapter)

        red_x, red_y = self.maze_adapter.corners[0]
        red_px, red_py = self.maze_adapter.cell_to_pixel(red_x, red_y)
        blue_x, blue_y = self.maze_adapter.corners[1]
        blue_px, blue_py = self.maze_adapter.cell_to_pixel(blue_x, blue_y)
        pink_x, pink_y = self.maze_adapter.corners[2]
        pink_px, pink_py = self.maze_adapter.cell_to_pixel(pink_x, pink_y)
        orange_x, orange_y = self.maze_adapter.corners[3]
        orange_px, orange_py = self.maze_adapter.cell_to_pixel(
            orange_x, orange_y
        )
        self.red_ghost = RedGhost(
            red_x, red_y, red_px, red_py, 2, self.maze_adapter
        )
        self.blue_ghost = PinkGhost(
            blue_x, blue_y, blue_px, blue_py, 2, self.maze_adapter
        )
        self.orange_ghost = OrangeGhost(
            orange_x, orange_y, orange_px, orange_py, 2, self.maze_adapter
        )
        self.pink_ghost = BlueGhost(
            pink_x, pink_y, pink_px, pink_py, 2, self.maze_adapter
        )
        self.player_images = [
            "assets/player_images/1.png",
            "assets/player_images/2.png",
            "assets/player_images/3.png",
        ]
        self.player_image = "assets/player_images/1.png"

    def eject_player_from_walls(self):
        if (
            self.maze_adapter.walls[self.player.cell_y][self.player.cell_x]
            == 15
        ):
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

    def check_win(self):
        super_pacgum_zero = sum(
            sublist.count(0) for sublist in self.maze_adapter.super_pacgum
        )
        pacgum_zero = sum(
            sublist.count(0) for sublist in self.maze_adapter.pacgum
        )
        if super_pacgum_zero == (
            self.maze_adapter.width * self.maze_adapter.height
        ) and pacgum_zero == (
            self.maze_adapter.width * self.maze_adapter.height
        ):
            return True
        return False

    def _load_images(self):
        pass

    def _handle_events(self, current_state, selected_index, menu_options):
        """Processes the pygame event queue for one frame. Returns the
        (possibly updated) running flag, game state, and menu selection."""
        running = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if current_state == GameState.MAIN_MENU:
                    if event.key == pygame.K_UP:
                        selected_index = (selected_index - 1) % len(
                            menu_options
                        )
                    elif event.key == pygame.K_DOWN:
                        selected_index = (selected_index + 1) % len(
                            menu_options
                        )
                    elif event.key == pygame.K_RETURN:
                        if selected_index == 0:
                            current_state = GameState.PLAYING
                        elif selected_index == 1:
                            current_state = GameState.CREDITSindex
                        elif selected_index == 2:
                            current_state = GameState.SETTINGS
                        elif selected_index == 3:
                            running = False

                elif current_state in [
                    GameState.PLAYING,
                    GameState.CREDITS,
                    GameState.SETTINGS,
                ]:
                    if event.key == pygame.K_ESCAPE:
                        current_state = GameState.MAIN_MENU

        return running, current_state, selected_index

    def _render_main_menu(
        self,
        menu_bg,
        menu_font,
        menu_options,
        selected_index,
        screen_width,
        screen_height,
    ):
        self.screen.blit(menu_bg, (0, 0))
        title_surface = menu_font.render("PAC-MAN 42", True, (0, 255, 255))
        self.screen.blit(
            title_surface,
            (screen_width // 2 - 100, screen_height // 2 - 100),
        )

        for index, option in enumerate(menu_options):
            if index == selected_index:
                color = (255, 255, 0)
            else:
                color = (255, 255, 255)

            text_surface = menu_font.render(option, True, color)

            x_pos = screen_width // 2 - 70
            y_pos = (screen_height // 2 - 20) + (index * 50)

            self.screen.blit(text_surface, (x_pos, y_pos))

    def _render_credits(self, menu_font, screen_width, screen_height):
        self.screen.fill("black")
        title_surface = menu_font.render("42 PAC-MAN", True, (0, 255, 255))
        self.screen.blit(
            title_surface,
            (screen_width // 2 - 100, screen_height // 2 - 150),
        )

    def _draw_maze_and_pickups(self):
        for row_index, row in enumerate(self.maze_adapter.walls):
            for col_index, cell_value in enumerate(row):
                pac_px, pac_py = self.maze_adapter.cell_to_pixel(
                    col_index, row_index
                )
                if self.maze_adapter.pacgum[row_index][col_index] == 1:
                    pygame.draw.circle(
                        self.screen,
                        (255, 255, 255),
                        (
                            pac_px + self.cell_size // 2,
                            pac_py + self.cell_size // 2,
                        ),
                        self.cell_size // 10,
                    )
                if self.maze_adapter.super_pacgum[row_index][col_index] == 1:
                    pygame.draw.circle(
                        self.screen,
                        (255, 255, 255),
                        (
                            pac_px + self.cell_size // 2,
                            pac_py + self.cell_size // 2,
                        ),
                        self.cell_size // 5,
                    )
                self.maze_adapter._render_maze(
                    cell_value, col_index, row_index, self.screen
                )

    def _draw_ghost_sprites(self):
        self.screen.blit(
            self.red_ghost.sprite,
            (
                self.red_ghost.pixel_x + self.cell_size // 8,
                self.red_ghost.pixel_y + self.cell_size // 8,
            ),
        )
        self.screen.blit(
            self.pink_ghost.sprite,
            (
                self.pink_ghost.pixel_x + self.cell_size // 8,
                self.pink_ghost.pixel_y + self.cell_size // 8,
            ),
        )
        self.screen.blit(
            self.blue_ghost.sprite,
            (
                self.orange_ghost.pixel_x + self.cell_size // 8,
                self.orange_ghost.pixel_y + self.cell_size // 8,
            ),
        )
        self.screen.blit(
            self.orange_ghost.sprite,
            (
                self.blue_ghost.pixel_x + self.cell_size // 8,
                self.blue_ghost.pixel_y + self.cell_size // 8,
            ),
        )

    def _read_player_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.player.next_dir = 1
        elif keys[pygame.K_s]:
            self.player.next_dir = 4

        if keys[pygame.K_a]:
            self.player.next_dir = 8
        elif keys[pygame.K_d]:
            self.player.next_dir = 2

    def _update_entities(self, delta_time):
        self.player.update(delta_time, self)
        self.red_ghost.update(delta_time, self.player)
        self.blue_ghost.update(delta_time, self.player)
        self.orange_ghost.update(delta_time, self.player)
        self.pink_ghost.update(delta_time, self.player)

    def _apply_ghost_mode(self):
        if self.super_power:
            self.red_ghost.scare_mode()
            self.blue_ghost.scare_mode()
            self.orange_ghost.scare_mode()
            self.pink_ghost.scare_mode()
        else:
            self.red_ghost.normal_mode("assets/ghost_images/red.png")
            self.blue_ghost.normal_mode("assets/ghost_images/blue.png")
            self.orange_ghost.normal_mode("assets/ghost_images/orange.png")
            self.pink_ghost.normal_mode("assets/ghost_images/pink.png")

    def _update_playing(self, delta_time):
        """Renders and updates one frame of gameplay. Returns False when
        the win condition is hit (so the caller can stop the loop)."""
        self.screen.fill((0, 0, 0))

        self._draw_maze_and_pickups()
        self._draw_ghost_sprites()

        self._read_player_input()

        self.player.draw_player(self.player_image)
        self.screen.blit(
            self.player.sprite,
            (
                self.player.pixel_x + self.cell_size // 6,
                self.player.pixel_y + self.cell_size // 6,
            ),
        )

        self._update_entities(delta_time)
        self._apply_ghost_mode()

        if self.check_win():
            print("YOU WIN")
            return False

        return True

    def _game_loop(self):
        running = True
        clock = pygame.time.Clock()
        current_state = GameState.MAIN_MENU
        menu_options = ["PLAY", "CREDITS", "SETTINGS", "QUIT"]

        menu_font = pygame.font.Font("ByteBounce.ttf", 48)
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()

        menu_bg = pygame.image.load("credits.jpg").convert()
        menu_bg = pygame.transform.scale(
            menu_bg, (screen_width, screen_height)
        )
        selected_index = 0
        self.eject_player_from_walls()

        while running:
            delta_time = clock.tick(60) / 1000.0

            running, current_state, selected_index = self._handle_events(
                current_state, selected_index, menu_options
            )

            if current_state == GameState.MAIN_MENU:
                self._render_main_menu(
                    menu_bg,
                    menu_font,
                    menu_options,
                    selected_index,
                    screen_width,
                    screen_height,
                )
            elif current_state == GameState.PLAYING:
                if not self._update_playing(delta_time):
                    running = False
                    continue
            elif current_state == GameState.SETTINGS:
                self.screen.blit(menu_bg, (0, 0))
            elif current_state == GameState.CREDITS:
                self._render_credits(menu_font, screen_width, screen_height)

            pygame.display.flip()

        pygame.quit()
