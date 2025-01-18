import os
import random
import sys
import time

from Common import *
from InGameState import InGameState
from BackgroundObject import BackgroundObject
from MainMenuState import MainMenuState
from EndState import EndState
from Button import Button

class Engine:
    _instance = None

    def __new__(cls, *args, **kwargs):
        """
        Singleton pattern implementation.

        Returns:
            Engine: The instance of the Engine.
        """
        if not cls._instance:
            cls._instance = super(Engine, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        """ Initializes the Engine. """
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pg.time.Clock()
        self.frame_per_sec = 60.0

        self.background_objects = []
        
        # resources
        self.background = pg.image.load(BACKGROUND_PATH)
        self.scroll_x = 0
        self.scroll_y = 0
        self.background_x = 0

        self.sprites = []
        self.stars_sprites = []
        self.asteroids_sprites = []

        self.game_over = None
        self.pause = False
        self.points = 0

        self.__init_time_variables()
        self.__load_images(self.stars_sprites, STARS_PATH)
        self.__load_images(self.asteroids_sprites, ASTEROIDS_PATH)
        self.__spawn_init_stars()
        
        self.all_states = {GameStateID.MAIN_MENU: MainMenuState(GameStateID.MAIN_MENU),
                               GameStateID.GAME: InGameState(GameStateID.GAME),
                               GameStateID.GAME_OVER: EndState(GameStateID.GAME_OVER)}
        self.current_state = self.all_states[GameStateID.MAIN_MENU]

        self.return_to_menu_bttn = None


    def run(self):
        """ Main loop of the game."""
        while True:
            self.__handle_events()
            self.screen.fill(BACKGROUND_COLOR)
            self.clock.tick(self.frame_per_sec)
            delta_time = 1.0 / self.frame_per_sec
            self.__update(delta_time)
            self.__scroll_background()
            self.__render()
            # update the display
            pg.display.flip()

    
    def add_object(self, game_object):
        """
        Adds a game object to the current state. It is used when current state is GAME.

        Args:
            game_object (GameObject): The object to add.
        """
        self.current_state.add_object(game_object)

        
    def get_ship_position(self):
        """
        Get the ship position. It is used when current state is GAME.

        Returns:
            pg.Vector2: The ship position.
        """
        return self.current_state.get_ship_position()

    
    def change_game_state(self, state_id):
        """
        Changes the current game state.

        Args:
            state_id (GameStateID): The ID of the new state
        """
        if state_id is not GameStateID.GAME_OVER:
            self.__restart_game()
        self.current_state = self.all_states[state_id]
        self.current_state.__init__(state_id)


    def set_game_over(self, game_over):
        """
        Sets the game over state.

        Args:
            game_over (bool): True if the game is over and player has won, False if the game is over and player has lost.
        """
        self.game_over = game_over
        self.change_game_state(GameStateID.GAME_OVER)


    def get_end_state(self):
        """
        Get the end state.

        Returns:
            bool: True if the game is over and player has won, False if the game is over and player has lost.
        """
        return self.game_over
    

    def add_points(self, points):
        """
        Adds points to the player.

        Args:
            points (int): The points to add.
        """
        self.points += points


    def get_points(self):
        """
        Get the current points of the player.

        Returns:
            int: The current points of the player.
        """
        return self.points
    

    def __restart_game(self):
        """ Restarts the game variables. """
        self.pause = False
        self.points = 0
        self.game_over = None


    def __draw_pause(self):
        """ Draws the pause screen. """
        rect_size = pg.Vector2(400, 200)
        bttn_size = pg.Vector2(100, 50)
        offset_x = 200
        offset_y = 50

        # draw pause text
        pg.font.init()
        font = pg.font.SysFont(DEFAULT_FONT_NAME, 70)
        text = font.render("PAUSE", True, COLOR_WHITE)
        pg.draw.rect(self.screen, RECT_DEFAULT_COLOR, (SCREEN_WIDTH / 2 - offset_x, SCREEN_HEIGHT / 2 - offset_y, rect_size.x, rect_size.y))    
        text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        self.screen.blit(text, text_rect)

        # draw border
        pg.draw.rect(self.screen, COLOR_WHITE, (SCREEN_WIDTH / 2 - offset_x, SCREEN_HEIGHT / 2 - offset_y, rect_size.x, rect_size.y), 3)

        # draw button
        bttn_pos = pg.Vector2(SCREEN_WIDTH / 2 - 50, SCREEN_HEIGHT / 2 + 75)
        self.return_to_menu_bttn = Button(bttn_pos, pg.Vector2(bttn_size), "MENU", lambda: self.change_game_state(GameStateID.MAIN_MENU))
        self.return_to_menu_bttn.draw(self.screen)

        self.screen.blit(text, text_rect)


    def __handle_events(self):
        """ Handles the events of the game. """
        events = pg.event.get()
        if self.pause == False:
            self.current_state.handle_events(events)
        for event in events:
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE and self.current_state.ID == GameStateID.GAME:
                self.pause = not self.pause
            if event.type == pg.KEYDOWN and event.key == pg.K_p and self.current_state.ID == GameStateID.GAME:
                self.current_state.ship.update_health(-100)


    def __render(self):
        """ Renders the game. """
        self.current_state.render(self.screen)
        if self.pause:
            self.__draw_pause()


    def __update(self, delta_time):   
        """ 
        Updates the game. 

        Args:
            delta_time (float): The time passed since the last frame in seconds.
        
        """       
        if self.return_to_menu_bttn is not None and self.pause == True:
            self.return_to_menu_bttn.update()

        if self.pause == True:
            return
        
        current_time = time.time()
        self.__spawn_time_objects(current_time)
        self.current_state.update(delta_time)

        for background_object in self.background_objects:
            background_object.update(delta_time)


    def get_sprite(self, sprite_name):
        """
        Get the sprite from the list of sprites. If the sprite is not found, it is loaded.

        Args:
            sprite_name (str): The name of the sprite.

        Returns:
            pg.Surface: The sprite. None if the sprite is not found.
        """
        # find the sprite
        if self.sprites is not None and sprite_name in self.sprites:
            return self.sprites[self.sprites.index(sprite_name)]
        # else load the sprite
        sprite = pg.image.load(sprite_name)
        if sprite is None:
            return None
        self.sprites.append(sprite)
        return sprite


    def __scroll_background(self):
        """  Scrolls the background of the game to create effect of movement. """
        if self.pause == False and self.current_state.ID is not GameStateID.MAIN_MENU:
            # Scroll the background horizontally
            self.scroll_y += 1
        
        # Draw the background twice to create seamless scrolling effect
        self.screen.blit(self.background, (self.scroll_x, self.scroll_y))
        self.screen.blit(self.background, (self.scroll_x, self.scroll_y - self.background.get_height()))

        # Reset the background position when it goes off screen
        if self.scroll_y >= self.background.get_height():
            self.scroll_y = 0


    def __spawn_time_objects(self, current_time):
        """
        Spawns objects based on time.

        Args:
            current_time (float): The current time in seconds.
        """
        # check if it is time to spawn a new background object
        if current_time - self.last_asteroid_spawn_time >= self.asteroid_spawn_time:
            self.__spawn_asteroids()
            self.last_asteroid_spawn_time = current_time

        # check if it is time to spawn stars
        if current_time - self.last_stars_spawn_time >= self.stars_spawn_time:
            self.__spawn_stars()
            self.last_stars_spawn_time = current_time


    def __spawn_background_object(self, sprite_list, position, size_range, depth_range, color=None):
        """
        Spawns a generic background object.

        Args:
            sprite_list (dict): Dictionary of sprites to choose from.
            position (pg.Vector2): Initial position of the object.
            size_range (tuple): Minimum and maximum size of the object (min_size, max_size).
            depth_range (tuple): Minimum and maximum depth of the object (min_depth, max_depth).
            color (pg.Color): Color of the object.
        """
        depth = random.randint(*depth_range)
        size = random.randint(*size_range)
        sprite_image = random.choice(sprite_list)
        background_object = BackgroundObject(position, sprite_image, pg.Vector2(size, size), depth, color)
        self.background_objects.append(background_object)


    def __spawn_asteroids(self):
        """Spawns an asteroid."""
        size_range = (ASTEROID_MIN_SIZE, ASTEROID_MAX_SIZE)
        depth_range = (1, 2)
        x_position = random.randint(2 * size_range[1], SCREEN_WIDTH - 2 * size_range[1])
        position = pg.Vector2(x_position, -size_range[1])
        self.__spawn_background_object(self.asteroids_sprites, position, size_range, depth_range)


    def __spawn_star(self, position):
        """Spawns a single star at the specified position."""
        color=None
        rand_color = random.randint(1, 4)

        if rand_color == 1:
            color = random.choice(STAR_COLORS)
        size_range = (STAR_MIN_SIZE, STAR_MAX_SIZE)
        depth_range = (1, 2)
        self.__spawn_background_object(self.stars_sprites, position, size_range, depth_range, color)


    def __spawn_init_stars(self):
        """Spawns initial stars randomly across the screen."""
        for _ in range(25):
            x_position = random.randint(STAR_MAX_SIZE, SCREEN_WIDTH - STAR_MAX_SIZE)
            y_position = random.randint(STAR_MAX_SIZE, SCREEN_HEIGHT - STAR_MAX_SIZE)
            self.__spawn_star(pg.Vector2(x_position, y_position))


    def __spawn_stars(self):
        """Spawns a new star at the top of the screen."""
        x_position = random.randint(STAR_MAX_SIZE, SCREEN_WIDTH - STAR_MAX_SIZE)
        y_position = -STAR_MAX_SIZE
        self.__spawn_star(pg.Vector2(x_position, y_position))


    def __init_time_variables(self):
        """ Initializes the time variables. """
        self.last_asteroid_spawn_time = time.time()
        self.asteroid_spawn_time = 3

        self.last_stars_spawn_time = time.time()
        self.stars_spawn_time = 0.2


    def __load_images(self, array, dir_path):
        """ 
        Loads images from a directory and stores them in an array.

        Args:
            array (list): The array to store the images.
            dir_path (str): The path to the directory.
        """
        for root, dirs, files in os.walk(dir_path):
            for file in files:
                if file.endswith((".png", ".jpg", ".jpeg")):
                    path = os.path.join(root, file)
                    img = pg.image.load(path)
                    array.append(img)
