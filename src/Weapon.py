from DynamicObject import DynamicObject

class Weapon(DynamicObject):
    def __init__(self, position, sprite):
        super().__init__(position, sprite)

        self.dealing_damage = 10
        self.dead_by_collision = True
        self.is_owned_by_player = False
        

    def set_ownership(self, is_owned_by_player):
        self.is_owned_by_player = is_owned_by_player

    def is_owned_by_player(self):
        return self.is_owned_by_player

    def set_dealing_damage(self, damage):
        self.dealing_damage = damage

    def get_dealing_damage(self):
        return self.dealing_damage