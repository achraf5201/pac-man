import arcade
import random

class GameView(arcade.Window):
    def __init__(self):
        super().__init__(1920, 1080, "ael-bala")
        self.background_color = arcade.csscolor.NAVY

        self.player_texture = arcade.load_texture("player.png")
        self.red_gost_texture = arcade.load_texture("red_gost.png")
        self.orange_gost_texture = arcade.load_texture("orange_gost.png")
        self.blue_gost_texture = arcade.load_texture("blue_gost.png")
        self.green_gost_texture = arcade.load_texture("green_gost.png")

        self.player_sprite = arcade.Sprite(self.player_texture, scale=0.2)
        self.player_sprite.center_x = 960
        self.player_sprite.center_y = 540

        self.red_gost_sprite = arcade.Sprite(self.red_gost_texture, scale=0.2)
        self.red_gost_sprite.center_x = 100
        self.red_gost_sprite.center_y = 170

        self.orange_gost_sprite = arcade.Sprite(
            self.orange_gost_texture, scale=0.2
        )
        self.orange_gost_sprite.center_x = 1830
        self.orange_gost_sprite.center_y = 1000

        self.green_gost_sprite = arcade.Sprite(
            self.green_gost_texture, scale=0.2
        )
        self.green_gost_sprite.center_x = 1830
        self.green_gost_sprite.center_y = 170

        self.blue_gost_sprite = arcade.Sprite(
            self.blue_gost_texture, scale=0.2
        )
        self.blue_gost_sprite.center_x = 100
        self.blue_gost_sprite.center_y = 1000

        self.background_color = arcade.csscolor.CORNFLOWER_BLUE

        self.all_ghosts = [
            self.red_gost_sprite,
            self.orange_gost_sprite,
            self.green_gost_sprite,
            self.blue_gost_sprite,
        ]
        for ghost in self.all_ghosts:
            ghost.change_x = random.choice([-3, -2, 2, 3])
            ghost.change_y = random.choice([-3, -2, 2, 3])

    def setup(self):
        """Set up the game here. Call this function to restart the game."""
        pass

    def on_update(self, delta_time):
        """Movement and game logic goes here. This runs 60 times a second."""

        self.player_sprite.update()

        for ghost in self.all_ghosts:
            ghost.update()

            if ghost.left < 0 or ghost.right > 1920:
                ghost.change_x *= -1

            if ghost.bottom < 0 or ghost.top > 1080:
                ghost.change_y *= -1

    def on_draw(self):
        """Render the screen."""

        self.clear()

        arcade.draw_sprite(self.player_sprite)
        arcade.draw_sprite(self.orange_gost_sprite)
        arcade.draw_sprite(self.green_gost_sprite)
        arcade.draw_sprite(self.blue_gost_sprite)
        arcade.draw_sprite(self.red_gost_sprite)


d = GameView()
d.setup()
arcade.run()
