from Common import *

class Button:
    def __init__(self, position, size, text, action, font_size=15):
        """
        Creates a new button.

        Args:
            position (Vector2): The position of the button.
            size (Vector2): The size of the button.
            text (str): The text on the button.
            action (function): The action to be executed when the button is clicked.
            font_size (int): The font size of the text.
        """
        self.position = position
        self.size = size
        self.text = text
        self.action = action

        self.font_size = font_size
        self.font_color = (200, 200, 200)
        self.bg_color = (100,100,100)
        self.hover_color = (32, 32, 32)
        self.border_color = (255, 255, 255)

        pg.font.init()
        font = pg.font.SysFont(DEFAULT_FONT_NAME, self.font_size)
        self.text_surface = font.render(self.text, True, self.font_color)
        self.text_rect = self.text_surface.get_rect(center=(self.position.x + self.size.x / 2, self.position.y + self.size.y / 2))

        self.hovered = False
        self.mouse_pressed = False

    
    def set_bg_color(self, color):
        """
        Sets the background color of the button.

        Args:
            color (tuple): The color of the button.
        """
        self.bg_color = color

    
    def set_hover_color(self, color):
        """
        Sets the hover color of the button.

        Args:
            color (tuple): The hover color of the button.
        """
        self.hover_color = color

    
    def set_border_color(self, color):
        """
        Sets the border color of the button.

        Args:
            color (tuple): The border color of the button
        """
        self.border_color = color


    def set_font_color(self, color):
        """
        Sets the font color of the button.

        Args:
            color (tuple): The font color of the button.
        """
        self.font_color = color
        self.text_surface = self.font.render(self.text, True, self.font_color)


    def update(self):
        """ Updates the button logic. """
        self.hovered = self.__is_hovered()
        
        mouse_pressed = pg.mouse.get_pressed()[0]
        if self.hovered and mouse_pressed and not self.mouse_pressed:
            self.action()  
        self.mouse_pressed = mouse_pressed


    def draw(self, screen):
        """
        Draws the button.

        Args:
            screen (Surface): The screen to draw the button on.
        """
        if self.hovered:
            pg.draw.rect(screen, self.hover_color, (self.position.x, self.position.y, self.size.x, self.size.y))
        else:
            pg.draw.rect(screen, self.bg_color, (self.position.x, self.position.y, self.size.x, self.size.y))

        pg.draw.rect(screen, self.border_color, (self.position.x, self.position.y, self.size.x, self.size.y), 3)
        screen.blit(self.text_surface, self.text_rect)


    def __is_hovered(self):
        """ Checks if the mouse is hovering over the button. """
        mouse_pos = pg.mouse.get_pos()
        return self.position.x < mouse_pos[0] < self.position.x + self.size.x and self.position.y < mouse_pos[1] < self.position.y + self.size.y