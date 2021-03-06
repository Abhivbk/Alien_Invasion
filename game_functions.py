import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep

def check_keydown_events(event, ai_settings, screen, ship, bullets):
    """Respond to key presses."""

    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
        ship.moving_right = True

    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
        ship.moving_left = True

    elif event.key == pygame.K_SPACE:
        if len(bullets) < ai_settings.bullets_allowed:
            fire_bullet(ai_settings, screen, ship, bullets)

    elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
        sys.exit()


def check_keyup_events(event, ship):
    """Respond to key releases."""
    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
        ship.moving_left = False


def mouse_button_down(ai_settings, screen, ship, bullets):
    mouse_presses = pygame.mouse.get_pressed()
    if mouse_presses[0]:
        fire_bullet(ai_settings, screen, ship, bullets)


def fire_bullet(ai_settings, screen, ship, bullets):
    """Fire a bullet if limit not reached yet."""
    # Create a new bullet and add it to the bullets group.
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def check_events(ai_settings, screen, ship, bullets):
    """Respond to key presses and mouse events."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_button_down(ai_settings, screen, ship, bullets)

        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)


def update_screen(screen, ship, alien, bullets):
    # Redraw all bullets behind ship and aliens.
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    alien.draw(screen)

    pygame.display.flip()


def update_bullets(ai_settings, screen, ship, aliens, bullets):
    """Update position of bullets and get rid of old bullets."""
    # Update bullet positions.
    bullets.update()

    # Get rid of bullets that have disappeared.
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    # print(len(bullets))
    check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets)


def check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets):
    # Check for any bullets that have hit aliens.
    # If so, get rid of the bullet and the alien.
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    # Repopulating the Alien Fleet
    if len(aliens) == 0:
        # Increasing the Alien Movement Speed
        ai_settings.alien_speed_factor += 0.5
        # Destroying the other bullets
        bullets.empty()
        create_fleet(ai_settings, screen, aliens, ship)


def ship_hit(ai_settings, stats, screen, ship, aliens, bullets):
    if stats.ships_left > 0:
        """Respond to ship being hit by alien."""
        # Decrement ships_left.
        stats.ships_left -= 1

        # Empty the list of aliens and bullets.
        aliens.empty()
        bullets.empty()

        # Create a new fleet and center the ship.

        # A new fleet automatically gets created because as the aliens become because of "aliens.empty()"
        # repopulating the alien fleet gets triggerred in "check_bullet_alien_collisions()".

        ship.center_ship()

        # Pause.
        sleep(0.5)
    else:
        stats.game_active = False


''' ALIEN FUNCTIONS ????'''


def get_number_aliens_x(ai_settings, alien_width):
    """Determine the number of aliens that fit in a row."""

    ''' We leave margins on both side of screens.
            To ????Find The available space for aliens we subtract the Screen width by 2 times alien_width '''
    available_space_x = ai_settings.screen_width - (2 * alien_width)

    ''' We divide the available space with alien_width to find the number of aliens '''
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def get_number_rows(ai_settings, ship_height, alien_height):
    # Calculating how many rows of aliens can fit in the window
    available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """Create a full fleet of aliens."""
    # Create an alien and find the number of aliens in a row.
    # Spacing between each alien is equal to one alien width.
    alien = Alien(ai_settings, screen)

    alien_width = alien.rect.width
    alien_height = alien.rect.height

    # We keep shifting the alien towards the right with leaving some space between
    alien.x = alien_width + (2 * alien_width * alien_number)
    alien.rect.y = alien_height + 2 * alien_height * row_number

    aliens.add(alien)


def create_fleet(ai_settings, screen, aliens, ship):
    # Create the first row of aliens.
    alien = Alien(ai_settings, screen)

    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def check_fleet_edges(ai_settings, aliens):
    """ Respond Appropriately if any aliens reach the edge """
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    """ Drop the entire fleet and Change its Direction"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets):
    screen_rect = screen.get_rect()
    """ Check if any aliens have reached the bottom """
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Treat this the same as if the ship got hit.
            ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
            break


def update_aliens(ai_settings, stats, screen, ship, aliens, bullets):
    """ Check if the fleet is at an edge, and then update the positions of all aliens in the fleet. """
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # Look For alien-ship Collisions
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, ship, aliens, bullets)

    check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets)