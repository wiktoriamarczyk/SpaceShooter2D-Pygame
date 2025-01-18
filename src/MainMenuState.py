import random
from Common import *
from GameState import GameState
from Button import Button

class MainMenuState (GameState):
    def __init__(self, ID):
        super().__init__(ID)
        self.next_state = GameStateID.GAME

        self.title = "SPACE SHOOTER 2D"
        self.bttn_color = (255, 255, 255)
        self.time_to_change_color = 0.25
        self.timer = 0

        bttn_size = pg.Vector2(150, 75)
        bttn_pos = pg.Vector2(SCREEN_WIDTH / 2 - bttn_size.y, SCREEN_HEIGHT / 2)

        from Engine import Engine
        func = lambda: Engine._instance.change_game_state(GameStateID.GAME)
        self.play_bttn = Button(bttn_pos, pg.Vector2(150, 75), "PLAY", func, 30)


    def update(self, delta_time):
        self.play_bttn.update()
        self.timer += delta_time
        if self.timer >= self.time_to_change_color:
            self.timer = 0
            self.bttn_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            self.play_bttn.color = self.bttn_color


    def render(self, screen):
        offset_y = 100

        title_font = pg.font.SysFont(DEFAULT_FONT_NAME, 70)
        title_text = title_font.render(self.title, True, self.bttn_color)
        title_text_rect = title_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - offset_y))
        screen.blit(title_text, title_text_rect)

        author_font = pg.font.SysFont(DEFAULT_FONT_NAME, 15)
        author_text = author_font.render("Author: Wiktoria Marczyk", True, COLOR_WHITE)
        author_text_rect = author_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT - offset_y))
        screen.blit(author_text, author_text_rect)
        
        self.play_bttn.draw(screen)


    def handle_events(self, events):
        pass