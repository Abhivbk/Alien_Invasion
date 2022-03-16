class Settings:
    #  """A class to store all settings for Alien Invasion."""
    def __init__(self):
        #  """Initialize the game's settings."""
        # Screen settings
        self.screen_height = 650
        self.screen_width = 1000
        self.bg_color = (44, 42, 74)

        self.ship_speed_factor = 1.5

        # Bullet settings
        self.bullet_speed_factor = 1
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 230, 230, 230
