import pygame
#Adds Music to One Shot Mode
class Music:
    def __init__(self):
        pygame.mixer.init()
        self.game_music = pygame.mixer.Sound('/Users/ethanrizko/Desktop/python_work/Alien_Invasion_Game/Soul_Of_Cinder.mp3')
    def play_music(self):
        self.game_music.play(-1)
    def stop_music(self):
        self.game_music.stop()