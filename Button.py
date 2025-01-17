from Common import *

class Button:
    def __init__(self, position, size, text, action, font_size=20):
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
        self.font = pg.font.Font(None, self.font_size)
        self.text_surface = self.font.render(self.text, True, self.font_color)
        self.text_rect = self.text_surface.get_rect(center=(self.position.x + self.size.x / 2, self.position.y + self.size.y / 2))

        self.hovered = False
        self.mouse_pressed = False

    
    def set_bg_color(self, color):
        self.bg_color = color

    
    def set_hover_color(self, color):
        self.hover_color = color

    
    def set_border_color(self, color):
        self.border_color = color


    def set_font_color(self, color):
        self.font_color = color
        self.text_surface = self.font.render(self.text, True, self.font_color)


    def update(self):
        self.hovered = self.__is_hovered()
        
        mouse_pressed = pg.mouse.get_pressed()[0]
        if self.hovered and mouse_pressed and not self.mouse_pressed:
            self.action()  
        self.mouse_pressed = mouse_pressed


    def draw(self, screen):
        if self.hovered:
            pg.draw.rect(screen, self.hover_color, (self.position.x, self.position.y, self.size.x, self.size.y))
        else:
            pg.draw.rect(screen, self.bg_color, (self.position.x, self.position.y, self.size.x, self.size.y))

        pg.draw.rect(screen, self.border_color, (self.position.x, self.position.y, self.size.x, self.size.y), 3)
        screen.blit(self.text_surface, self.text_rect)


    def __is_hovered(self):
        mouse_pos = pg.mouse.get_pos()
        return self.position.x < mouse_pos[0] < self.position.x + self.size.x and self.position.y < mouse_pos[1] < self.position.y + self.size.y