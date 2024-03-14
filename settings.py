import pygame

class Settings:
    def __init__(self):
        self.screen_width = 1200
        self.screen_height = 700
        self.bg_color = (0, 0, 40)
        
        self.ship_limit = 3
        self.bullet_width = 2
        self.bullet_height = 15
        self.bullet_color = (235, 0, 50)
        self.bullets_allowed = 20
        
        self.fleet_drop_speed = 10

        self.speedup_scale = 1.1
       
       #Modification 1 pt 1: better score scaling for harder difficulties. 
        self.score_scale = 1.5
        self.medium_score_scale = 2
        self.hard_score_scale = 3
        self.one_shot_score_scale = 15
        
        self.initialize_dynamic_settings()

        #Modification 1 pt 2: higher point values for harder difficulties
        self.alien_points = 50
        self.medium_alien_points = 125
        self.hard_alien_points = 200
        self.one_shot_alien_points = 500
    
    def initialize_dynamic_settings(self):
        self.ship_speed = 10
        self.bullet_speed = 13
        self.alien_speed = 5
        self.fleet_direction = 1
    def increase_speed(self):
        self.ship_speed *= self.speedup_scale
        # self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)
        print(self.alien_points)