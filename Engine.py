from Common import *
from Ship import *
from Bullet import *

class Engine:
    def __init__(self):
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pg.time.Clock()
        self.frame_per_sec  = 60.0
        
        self.game_objects = []
        self.ship = None

        self.initialize_game_objects()


    def run(self):
        while True:
            self.handle_events()
            self.screen.fill(BACKGROUND_COLOR)
            self.clock.tick(self.frame_per_sec)
            delta_time = 1.0 / self.frame_per_sec
            self.update(delta_time)
            self.render()
            # Update the display
            pg.display.flip()


    def handle_events(self):
        for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.KEYUP:
                     if event.key == pg.K_SPACE:
                        self.fire_bullet()


    def render(self):
        for game_object in self.game_objects:
            game_object.render(self.screen)


    def update(self, delta_time):
        for game_object in self.game_objects:
            game_object.update(delta_time)

        # update only alive objects
        for go in self.game_objects:
            if go.alive == False:
                self.game_objects.remove(go)
                go.__del__()
    

    def fire_bullet(self):
        bullet_pos = self.ship.position
        bullet = Bullet(bullet_pos.x, bullet_pos.y + 5)
        self.game_objects.append(bullet)


    def initialize_game_objects(self):
        ship = Ship()
        self.ship = ship
        self.game_objects.append(ship)