class Settings:
    #  """A class to store all settings for Alien Invasion."""
    def __init__(self, screen):
        #  """Initialize the game's settings."""

        # Screen settings
        self.screen = screen
        self.screen_width, self.screen_height = self.screen.get_size()
        self.bg_color = (44, 42, 74)

        # Ship settings
        self.ship_speed_factor = 1.5

        # Bullet settings
        self.bullet_speed_factor = 1
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 230, 230, 230
        self.bullets_allowed = 3
