import pygame
from settings import Settings
from ship import Ship
import game_functions as gf
from pygame.sprite import Group
from alien import Alien


def run_game():
    pygame.init()
    bg_color = (44, 42, 74)

    ai_settings = Settings()

    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    ship = Ship(ai_settings, screen)

    # Make a group to store bullets in.
    bullets = Group()

    alien = Alien(ai_settings, screen)
    aliens = Group()

    # Create the fleet of aliens.
    gf.create_fleet(ai_settings, screen, aliens)

    while True:
        gf.check_events(ai_settings, screen, ship, bullets)
        ship.update()

        gf.update_bullets(bullets)

        gf.update_screen(ai_settings, screen, ship, aliens, bullets)
        screen.fill(ai_settings.bg_color)

        ship.blitme()


run_game()
