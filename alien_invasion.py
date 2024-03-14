import sys 
from time import sleep
import pygame
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_music import Music
 
class AlienInvasion:
    def __init__(self):
        pygame.init()
        self.game_active = False
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        # self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        self.ship = Ship(self)
        self.music = Music()
        self.play_button = Button(self, "Play")
        self._make_difficulty_level_button()
        self.bullets = pygame.sprite.Group()
        self.bullet = Bullet(self) #modification 2, automatic shooting: creates instance of Bullet class in __init__() in order to access shooting variable in bullet.py
        self.aliens = pygame.sprite.Group()
        self._create_fleet()
        self.bg_color = (0, 0, 40)
    
    def run_game(self):
        while True:
            self._check_events()
            if self.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            self._update_screen()
            self.clock.tick(60)
    
    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
                self._check_difficulty_buttons(mouse_pos)
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
    
    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_UP:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE: #Modification 2, automatic shooting. Changes value of variable within bullet.py to True
            self.bullet.shooting = True
    
    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False
        elif event.key == pygame.K_SPACE: #Modification 2, automatic shooting: Changes value of variable within bullet.py to False
            self.bullet.shooting = False
    
    def _fire_bullet(self):
        if (len(self.bullets) < self.settings.bullets_allowed) and self.bullet.shooting: #Modifcation 2, automatic shooting: sets condition that self.bullet.shooting = True in order for new bullet to be created.
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
            self.bullets.update()
    
    def _update_bullets(self):
        self.bullets.update()
        self._fire_bullet() #Modification 2, automatic shooting: places _fire_bullet() in _update_bullets(), which is called in the run_game() function to ensure that bullets are created continously when self.bullet.shooting = True.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collisions()
    
    def _check_bullet_alien_collisions(self):
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            self.stats.level += 1
            self.sb.prep_level()
    
    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)
        self.sb.show_score()
        if not self.game_active:
            self.play_button.draw_play_button()
            self.easy_button.draw_button()
            self.medium_button.draw_button()
            self.hard_button.draw_button()
            self.one_shot.draw_button()
        pygame.display.flip()
    
    def _create_fleet(self):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        current_x, current_y = alien_width, alien_height
        while current_y < (self.settings.screen_height - 6 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width
            current_x = alien_width
            current_y += 2 * alien_height
            self.aliens.add(alien)
    
    def _update_aliens(self):
        self._check_fleet_edges()
        self.aliens.update()
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
            print("ship hit!!!")
        self._check_aliens_bottom()
    
    def _create_alien(self, x_position, y_position):
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)
    
    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
   
    def _change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1
   
    def _ship_hit(self):
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            self.sb.prep_ships()
            self.bullets.empty()
            self.aliens.empty()
            self._create_fleet()
            self.ship.center_ship()
            sleep(0.5)
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)
    
    def _check_aliens_bottom(self):
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                self._ship_hit()
                break
    
    def _check_play_button(self, mouse_pos):
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()
            self.game_active = True
            self.bullets.empty()
            self.aliens.empty()
            self._create_fleet()
            self.ship.center_ship()
            pygame.mouse.set_visible(False)
    def _make_difficulty_level_button(self):
        self.easy_button = Button(self, "Easy")
        self.medium_button = Button(self, "Medium")
        self.hard_button = Button(self, "Hard")
        self.one_shot = Button(self, "One Shot")

        self.easy_button.rect.top = (self.play_button.rect.top + 1.5*self.play_button.rect.height)
        self.easy_button._update_msg_position()

        self.medium_button.rect.top = (self.easy_button.rect.top + 1.5*self.easy_button.rect.height)
        self.medium_button._update_msg_position()

        self.hard_button.rect.top = (self.medium_button.rect.top + 1.5*self.medium_button.rect.height)
        self.hard_button._update_msg_position()

        self.one_shot.rect.top = (self.hard_button.rect.top + 1.5*self.hard_button.rect.height)
        self.one_shot._update_msg_position()
    
    def _check_difficulty_buttons(self, mouse_pos):
        easy_button_clicked = self.easy_button.rect.collidepoint(mouse_pos)
        medium_button_clicked = self.medium_button.rect.collidepoint(mouse_pos)
        hard_button_clicked = self.hard_button.rect.collidepoint(mouse_pos)
        one_shot_clicked = self.one_shot.rect.collidepoint(mouse_pos)
        if easy_button_clicked:
            self.settings.speedup_scale = 1.1
            self.settings.bg_color = (0, 0, 40)
            self.settings.bullet_color = (235, 0, 50)
            self.music.game_music.stop()
            self.settings.ship_limit = 3
            self.sb.prep_high_score() 
        elif medium_button_clicked:
            self.settings.speedup_scale = 1.3
            
            #modification 1, all parts implemented
            self.settings.score_scale = self.settings.medium_score_scale
            self.settings.alien_points = self.settings.medium_alien_points
            self.settings.bg_color = (0, 0, 40)
            self.settings.bullet_color = (235, 0, 50)
            self.music.game_music.stop()
            self.settings.ship_limit = 3
            self.sb.prep_high_score()
        elif hard_button_clicked:
            self.settings.speedup_scale = 1.5
            
            #modification 1, all parts implemented
            self.settings.score_scale = self.settings.hard_score_scale
            self.settings.alien_points = self.settings.hard_alien_points
            self.settings.bg_color = (0, 0, 40)
            self.settings.bullet_color = (235, 0, 50)
            self.music.game_music.stop() 
            self.settings.ship_limit = 3
            self.sb.prep_high_score()
        elif one_shot_clicked: #modification 3: new, harder difficulty with better score but faster speedup, lower bullet limit, slower bullet speed, faster alien speed, no lives, music, and change in background and bullet color
            self.settings.speedup_scale = 2
            self.settings.score_scale = self.settings.one_shot_score_scale
            self.settings.alien_points = self.settings.one_shot_alien_points
            self.settings.ship_limit = 0
            self.settings.bullet_speed = 7
            self.settings.alien_speed = 10
            self.settings.bullets_allowed = 12
            self.music.play_music()
            self.settings.bg_color = (82, 7, 0)
            self.settings.bullet_color = (242, 212, 12)
            self.sb.prep_high_score()

if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()