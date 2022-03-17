import pygame
from settings import Settings
from ship import Ship
import game_functions as gf
from pygame.sprite import Group
from alien import Alien


def run_game():
    pygame.init()
    bg_color = (44, 42, 74)

    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption("Alien Invasion")

    # Initialising some things...
    ai_settings = Settings(screen)
    ship = Ship(ai_settings, screen)

    # Make a groups to store bullets and aliens in it.
    bullets = Group()
    aliens = Group()

    # Create the fleet of aliens.
    gf.create_fleet(ai_settings, screen, aliens, ship)

    while True:
        ''' First we check for keyboard inputs...'''
        gf.check_events(ai_settings, screen, ship, bullets)

        ''' Then as we get the keyboard inputs the ships changes position accordingly... (Still not drawn on screen with 
         changed position only position changed numerically in variables) '''
        ship.update()

        ''' Position of bullets is changed (only numerically), Delete the existing bullets which ran out of screen(To 
        save Memory) '''
        gf.update_bullets(bullets)

        ''' Finally, 🤗  we draw the bullets and ships on the screen '''
        gf.update_screen(ai_settings, screen, ship, aliens, bullets)
        screen.fill(ai_settings.bg_color)  # Just change the background colour


if __name__ == '__main__':
    run_game()
