from Common import *
from GameState import GameState
from Button import Button

class EndState (GameState):
    def __init__(self, ID):
        super().__init__(ID)
        self.next_state = GameStateID.MAIN_MENU

        from Engine import Engine
        game_over = Engine._instance.get_end_state()
        self.title = "YOU WIN!" if not game_over else "GAME OVER"
        self.title_color = (14, 210, 27) if not game_over else (210, 14, 14)

        bttn_size = pg.Vector2(150, 75)
        offset_y = 100
        bttn_pos = pg.Vector2(SCREEN_WIDTH / 2 - bttn_size.y, SCREEN_HEIGHT / 2 + offset_y)

        from Engine import Engine
        func = lambda: Engine._instance.change_game_state(GameStateID.MAIN_MENU)
        self.menu_bttn = Button(bttn_pos, pg.Vector2(150, 75), "MENU", func, 40)


    def update(self, delta_time):
        self.menu_bttn.update()


    def render(self, screen):
        offset_y = 100

        # draw title
        title_font = pg.font.Font(None, 80)
        title_text = title_font.render(self.title, True, self.title_color)
        title_text_rect = title_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - offset_y))
        screen.blit(title_text, title_text_rect)

        # draw points count
        from Engine import Engine
        points = Engine._instance.get_points()
        points_font = pg.font.Font(None, 40)
        points_text = points_font.render("Enemies defeated: " + str(points), True, COLOR_WHITE)
        points_text_rect = points_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        screen.blit(points_text, points_text_rect)


        self.menu_bttn.draw(screen)

    
    def handle_events(self, events):
        pass