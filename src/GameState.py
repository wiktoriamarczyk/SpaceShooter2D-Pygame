from Common import *

class GameState:
    def __init__(self, ID):
        """
        Initialize the game state with the given ID.

        Args:
            ID (GameStateID): The ID of the game state.
        """
        self.ID = ID
        self.next_state = GameStateID.UNKNOWN

    def update(self, delta_time):
        """  
        Update the game state. 
        
        Args:
            delta_time (float): The time passed since the last update.
        """
        pass

    def render(self, screen):
        """
        Render the game state to the screen.

        Args:
            screen (pg.Surface): The screen to render the game state to.
        """
        pass

    def on_key_down(self, key):
        """
        Handle key down events.

        Args:
            key (int): The key that was pressed.
        """
        pass

    def get_ID(self):
        """
        Get the ID of the game state.

        Returns:
            GameStateID: The ID of the game state.
        """
        return self.ID
    
    def get_next_state_ID(self):
        """
        Get the ID of the next game state.

        Returns:
            GameStateID: The ID of the next game state.
        """
        return self.next_state
