from Common import *

class GameState:
    def __init__(self, ID):
        self.ID = ID
        self.next_state = GameStateID.UNKNOWN

    def update(self):
        pass

    def render(self, screen):
        pass

    def on_key_down(self, key):
        pass

    def get_ID(self):
        return self.ID
    
    def get_next_state_ID(self):
        return self.next_state