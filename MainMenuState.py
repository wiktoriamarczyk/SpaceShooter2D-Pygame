from Common import *
from GameState import GameState

class MainMenuState (GameState):
    def __init__(self, ID):
        super().__init__(ID)
        self.next_state = GameStateID.GAME

        self.buttons = []

    def update(self, delta_time):
        pass

    def render(self, screen):
        pass

    def handle_events(self, events):
        pass