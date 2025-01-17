from Common import *
from GameState import GameState

class EndState (GameState):
    def __init__(self, ID):
        super().__init__(ID)
        self.next_state = GameStateID.MAIN_MENU