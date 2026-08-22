import arcade


class GameView(arcade.Window):
    def __init__(self):
        super().__init__(1920, 1080, "ael-bala")
        self.background_color = arcade.csscolor.NAVY

        self.player_texture = arcade.load_texture(
            "pac-man-computer-icons-clip-art-pac-man-e67e3c744dffbc65835e26bbe23c3453.png"
        )

        self.player_sprite = arcade.Sprite(self.player_texture, scale=0.05)
        self.player_sprite.center_x = 960
        self.player_sprite.center_y = 540

        self.background_color = arcade.csscolor.CORNFLOWER_BLUE

    def setup(self):
        """Set up the game here. Call this function to restart the game."""
        pass

    def on_draw(self):
        """Render the screen."""

        # Clear the screen to the background color
        self.clear()

        # Draw our sprites
        arcade.draw_sprite(self.player_sprite)

d = GameView()
d.setup()
arcade.run()
