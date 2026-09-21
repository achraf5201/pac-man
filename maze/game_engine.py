import pygame
from mazegenerator import MazeGenerator
from maze.maze_adapter import MazeAdapter
from maze.player import Player
from maze.ghosts import RedGhost, PinkGhost, BlueGhost, OrangeGhost
import math
from enum import Enum
import time

# hadi an7aydoha w andiro tssawer yloopi 3lihom
# def draw_filled_arc(
#     surface, color, center, radius, start_angle_deg, stop_angle_deg
# ):
#     """Draws a filled pie-slice/arc on a surface."""
#     points = [center]
#     for degree in range(start_angle_deg, stop_angle_deg + 1):
#         radians = math.radians(degree)

#         x = center[0] + radius * math.cos(radians)
#         y = center[1] - radius * math.sin(radians)

#         points.append((x, y))

#     if len(points) > 2:
#         pygame.draw.polygon(surface, color, points)


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
        self.player_images = [
            "assets/player_images/1.png",
            "assets/player_images/2.png",
            "assets/player_images/3.png",
            "assets/player_images/4.png"
        ]
        self.player_image = "assets/player_images/1.png"

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
            red_x,
            red_y,
            red_px,
            red_py,
            2,
            self.maze_adapter,
            "assets/ghost_images/red.png",
        )
        self.blue_ghost = BlueGhost(
            blue_x,
            blue_y,
            blue_px,
            blue_py,
            2,
            self.maze_adapter,
            "assets/ghost_images/blue.png",
        )
        self.orange_ghost = OrangeGhost(
            orange_x,
            orange_y,
            orange_px,
            orange_py,
            2,
            self.maze_adapter,
            "assets/ghost_images/orange.png",
        )
        self.pink_ghost = PinkGhost(
            pink_x,
            pink_y,
            pink_px,
            pink_py,
            2,
            self.maze_adapter,
            "assets/ghost_images/pink.png",
        )
        self.var = 0
        self.index = 0
        self.cheat_invincibility = False
        self.cheat_ghost_freeze = False
        self.cheat_speed = False
        self.force_win = False
        self.settings_index = 0

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
  
        running = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                
                # main_menu
                if current_state == GameState.MAIN_MENU:
                    if event.key == pygame.K_UP:
                        selected_index = (selected_index - 1) % len(menu_options)
                    elif event.key == pygame.K_DOWN:
                        selected_index = (selected_index + 1) % len(menu_options)
                    elif event.key == pygame.K_RETURN:
                        if selected_index == 0:
                            current_state = GameState.PLAYING
                        elif selected_index == 1:
                            current_state = GameState.CREDITS
                        elif selected_index == 2:
                            current_state = GameState.SETTINGS
                        elif selected_index == 3:
                            running = False

                # settings events
                elif current_state == GameState.SETTINGS:
                    if event.key == pygame.K_UP:
                        self.settings_index = (self.settings_index - 1) % len(self.settings_options)
                    elif event.key == pygame.K_DOWN:
                        self.settings_index = (self.settings_index + 1) % len(self.settings_options)
                    elif event.key == pygame.K_RETURN:
                        if self.settings_index == 0:
                            self.cheat_invincibility = not self.cheat_invincibility
                        elif self.settings_index == 1:
                            self.cheat_ghost_freeze = not self.cheat_ghost_freeze
                        elif self.settings_index == 2:
                            self.cheat_speed = not self.cheat_speed
                            self.player.speed = 8 if self.cheat_speed else 4
                        elif self.settings_index == 3:
                            self.life += 1
                        elif self.settings_index == 4:
                            self.force_win = True
                            current_state = GameState.PLAYING
                            self.settings_index = 0
                        elif self.settings_index == 5:
                            current_state = GameState.MAIN_MENU
                            self.settings_index = 0
                    elif event.key == pygame.K_ESCAPE:
                        current_state = GameState.MAIN_MENU
                        self.settings_index = 0

                # credits
                elif current_state == GameState.CREDITS:
                    if event.key == pygame.K_ESCAPE:
                        current_state = GameState.MAIN_MENU

                # playing
                elif current_state == GameState.PLAYING:
                    if event.key == pygame.K_ESCAPE:
                        current_state = GameState.MAIN_MENU
                    elif event.key == pygame.K_p:
                        current_state = GameState.PAUSE
                
                # pause
                elif current_state == GameState.PAUSE:
                    if event.key == pygame.K_p:
                        current_state = GameState.PLAYING

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
                self.blue_ghost.pixel_x + self.cell_size // 8,
                self.blue_ghost.pixel_y + self.cell_size // 8,
            ),
        )
        self.screen.blit(
            self.orange_ghost.sprite,
            (
                self.orange_ghost.pixel_x + self.cell_size // 8,
                self.orange_ghost.pixel_y + self.cell_size // 8,
            ),
        )

    def _read_player_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.player.next_dir = 1
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.player.next_dir = 4

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.player.next_dir = 8
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.player.next_dir = 2

    def _update_entities(self, delta_time):
        self.player.update(delta_time, self)
        
        if not self.cheat_ghost_freeze:
            self.red_ghost.update(delta_time, self.player)
            self.blue_ghost.update(delta_time, self.player)
            self.orange_ghost.update(delta_time, self.player)
            self.pink_ghost.update(delta_time, self.player)

    def _apply_ghost_mode(self):
        if self.super_power:
            if not self.red_ghost.return_in_life:
                self.red_ghost.scare_mode()
            else:
                self.red_ghost.normal_mode()
            if not self.blue_ghost.return_in_life:
                self.blue_ghost.scare_mode()
            else:
                self.blue_ghost.normal_mode()
            if not self.orange_ghost.return_in_life:
                self.orange_ghost.scare_mode()
            else:
                self.orange_ghost.normal_mode()
            if not self.pink_ghost.return_in_life:
                self.pink_ghost.scare_mode()
            else:
                self.pink_ghost.normal_mode()
        else:
            self.red_ghost.return_in_life = False
            self.orange_ghost.return_in_life = False
            self.blue_ghost.return_in_life = False
            self.pink_ghost.return_in_life = False

            self.red_ghost.normal_mode()
            self.blue_ghost.normal_mode()
            self.orange_ghost.normal_mode()
            self.pink_ghost.normal_mode()

    def _update_playing(self, delta_time):
        """Renders and updates one frame of gameplay. Returns False when
        the win condition is hit (so the caller can stop the loop)."""
        self.screen.fill((0, 0, 0))

        self._draw_maze_and_pickups()
        self._draw_ghost_sprites()

        self._read_player_input()
        self.var += delta_time
        if self.var >= 0.1:
            self.var = 0
            self.index = (self.index + 1) % len(self.player_images)
            self.player.draw_player(self.player_images[self.index])
        else:
            self.player.draw_player(self.player_images[self.index])
        self.screen.blit(
            self.player.sprite,
            (
                self.player.pixel_x + self.cell_size // 6,
                self.player.pixel_y + self.cell_size // 6,
            ),
        )

        self._update_entities(delta_time)
        self._apply_ghost_mode()

        if self.check_win() or self.force_win:
            print("YOU WIN")
            self.force_win = False
            return False

        return True

    def _draw_gameplay(self):
        self.screen.fill((0, 0, 0))
        self._draw_maze_and_pickups()
        self._draw_ghost_sprites()
        self.player.draw_player(self.player_images[self.index])
        self.screen.blit(
            self.player.sprite,
            (
                self.player.pixel_x + self.cell_size // 6,
                self.player.pixel_y + self.cell_size // 6,
            ),
        )
    
    def _render_pause_menu(self, menu_font, screen_width, screen_height):
        self._draw_gameplay() 
        
        overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))
        
        pause_surface = menu_font.render("PAUSED", True, (255, 255, 255))
        self.screen.blit(
            pause_surface,
            (screen_width // 2 - 80, screen_height // 2 - 50),
        )


    def _render_settings(self, menu_bg, menu_font, screen_width, screen_height):
        self.screen.blit(menu_bg, (0, 0))
        title_surface = menu_font.render("CHEAT MODE (PEER REVIEW)", True, (0, 255, 255))
        self.screen.blit(
            title_surface,
            (screen_width // 2 - 200, screen_height // 2 - 250),
        )

        self.settings_options = [
            f"1. INVINCIBILITY: {'ON' if self.cheat_invincibility else 'OFF'}",
            f"2. GHOST FREEZE: {'ON' if self.cheat_ghost_freeze else 'OFF'}",
            f"3. INCREASED SPEED: {'ON' if self.cheat_speed else 'OFF'}",
            "4. ADD EXTRA LIFE (+1)",
            "5. SKIP LEVEL (INSTANT WIN)",
            "BACK"
        ]

        for index, option in enumerate(self.settings_options):
            if index == self.settings_index:
                color = (255, 255, 0)
            else:
                color = (255, 255, 255)

            text_surface = menu_font.render(option, True, color)
            x_pos = screen_width // 2 - 180
            y_pos = (screen_height // 2 - 150) + (index * 50)

            self.screen.blit(text_surface, (x_pos, y_pos))


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
                self._render_settings(menu_bg, menu_font, screen_width, screen_height)


            elif current_state == GameState.CREDITS:
                self._render_credits(menu_font, screen_width, screen_height)
            
            elif current_state == GameState.PLAYING:
                self.maze_adapter._render_hud(
                    self.screen, 
                    score=self.score, 
                    lives=self.life, 
                    level=self.level
                )
            
            elif current_state == GameState.PAUSE:
                print("we here pause")
                self._render_pause_menu(menu_font, screen_width, screen_height)

            pygame.display.flip()

        pygame.quit()
