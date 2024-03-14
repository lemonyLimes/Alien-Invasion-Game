class GameStats:
    def __init__(self, ai_game):
        self.settings = ai_game.settings
        self.reset_stats()
        with open('/Users/ethanrizko/Desktop/python_work/Alien_Invasion_Game/highscore.txt', 'r') as file:
            self.high_score = int(file.read())
    def reset_stats(self):
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1