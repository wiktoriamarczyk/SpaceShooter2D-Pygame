from DynamicObject import DynamicObject

class Weapon(DynamicObject):
    def __init__(self, position, sprite):
        super().__init__(position, sprite)

        self.dealing_damage = 10
        self.dead_by_collision = True
        self.is_owned_by_player = False
        

    def set_ownership(self, is_owned_by_player):
        """
        Set the ownership of the weapon.

        Args:
            is_owned_by_player (bool): True if the weapon is owned by the player, False otherwise
        """
        self.is_owned_by_player = is_owned_by_player

    def is_owned_by_player(self):
        """
        Returns the ownership of the weapon.

        Returns:
            bool: True if the weapon is owned by the player, False otherwise
        """
        return self.is_owned_by_player

    def set_dealing_damage(self, damage):
        """
        Set the damage that the weapon deals.

        Args:
            damage (int): The damage that the weapon deals
        """
        self.dealing_damage = damage

    def get_dealing_damage(self):
        """
        Returns the damage that the weapon deals.

        Returns:
            int: The damage that the weapon deals
        """
        return self.dealing_damage