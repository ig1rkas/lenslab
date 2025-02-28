import pygame
from config import *
from math import sin, radians


class TextInputBox:
    def __init__(self, start_value, width, x, y):
        self.start_width = width
        self.width = width
        self.screen = pygame.Surface((width, 30))
        self.rect = pygame.rect.Rect(x, y, width, 30)
        self.value = start_value
        self.selected = 0
        self.update()

    def print_text(self, message, font_color=BLACK, font_size=20, font_type=ROBOTO, degree=0):
        self.font_type = pygame.font.Font(font_type, font_size)
        self.text = self.font_type.render(message, True, font_color)
        self.text = pygame.transform.rotate(self.text, degree)
        if self.text.get_rect().width + 10 > self.width:
            self.width = self.text.get_rect().width + 10
            self.screen = pygame.Surface((self.width, 30))
            self.screen.fill(GRAY)
            pygame.draw.line(
                self.screen, GREEN if self.selected else BLACK, (0, 28), (self.width, 28), 2)
        if self.width - 10 >= self.text.get_rect().width > self.start_width:
            self.width -= 10
            self.screen = pygame.Surface((self.width, 30))
            self.screen.fill(GRAY)
            pygame.draw.line(
                self.screen, GREEN if self.selected else BLACK, (0, 28), (self.width, 28), 2)

        self.screen.blit(
            self.text, ((self.width - self.text.get_width()) / 2, 0))

    def add_value(self, value: str):
        self.value += value
        self.update()

    def backspace(self):
        self.value = self.value[:-1]
        self.update()

    def update(self):
        self.screen.fill(GRAY)
        pygame.draw.line(
            self.screen, GREEN if self.selected else BLACK, (0, 28), (self.width, 28), 2)
        self.print_text(self.value)


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SIZE)
        self.running = 1

        self.boxes = [
            TextInputBox("1", 40, 77, 20),  # height
            TextInputBox("1", 40, 77, 70),  # F1
            TextInputBox("1", 40, 77, 120),  # F2
        ]

        self.object_h = 1
        self.object_x = 140
        self.object_selected = 0

        self.lense1_x = 280
        self.lense1_selected = 0

        self.scale = 1

    def update_objects(self):
        self.object = pygame.rect.Rect(self.object_x, 720 / 2 - 1 - 250 * self.object_h, 3, 250 * self.object_h)
        self.lense1 = pygame.rect.Rect(self.lense1_x, 720 / 2 - 1 - 300, 3, 600)

    def print_text(self, x, y, message, font_color=BLACK, font_size=20, font_type=ROBOTO, degree=0):
        self.font_type = pygame.font.Font(font_type, font_size)
        self.text = self.font_type.render(message, True, font_color)
        self.text = pygame.transform.rotate(self.text, degree)
        self.screen.blit(self.text, (x, y))

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for tib in self.boxes:
                        if tib.rect.collidepoint(*event.pos):
                            tib.selected = 1
                            tib.update()
                        else:
                            tib.selected = 0
                            tib.update()
                    if self.object.collidepoint(*event.pos):
                        self.object_selected = not self.object_selected
                        
                    if self.lense1.collidepoint(*event.pos):
                        self.lense1_selected = not self.lense1_selected

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    for tib in self.boxes:
                        if tib.selected:
                            tib.backspace()
                elif event.key == pygame.K_RETURN:
                    for tib in self.boxes:
                        tib.selected = 0
                        tib.update()
                    self.object_selected = 0
                    self.lense1_selected = 0
                else:
                    for tib in self.boxes:
                        if tib.selected:
                            tib.add_value(event.unicode)

    def update(self):
        try:
            if self.boxes[0].value:
                self.object_h = float(self.boxes[0].value)
            else:
                self.object_h = 0
        except Exception:
            self.boxes[0].value = "1"
            self.object_h = 1

        if self.object_selected:
            self.object_x = pygame.mouse.get_pos()[0]
        if self.lense1_selected:
            self.lense1_x = pygame.mouse.get_pos()[0]
        self.update_objects()

    def render(self):
        self.screen.fill(GRAY)
        self.print_text(10, 20, "H, m = ", font_size=20)
        self.print_text(10, 70, "F1, m = ", font_size=20)
        self.print_text(10, 120, "F2, m = ", font_size=20)

        for tib in self.boxes:
            self.screen.blit(tib.screen, (tib.rect.x, tib.rect.y))

        pygame.draw.line(self.screen, BLACK, (0, 720 / 2 - 1), (1280, 720 / 2 - 1), 2)
        
        pygame.draw.rect(self.screen, object_arrow_color := (GREEN if self.object_selected else BLACK), self.object)
        pygame.draw.line(self.screen, object_arrow_color, (self.object.x - 10, self.object.y + 10), (self.object.x, self.object.y), 4)
        pygame.draw.line(self.screen, object_arrow_color, (self.object.x + 10, self.object.y + 10), (self.object.x, self.object.y), 4)
        
        self.print_text(self.object.x + 20, self.object.y + self.object.height / 2, message="H")
        
        pygame.draw.rect(self.screen, lense1_arrow_color := (GREEN if self.lense1_selected else BLACK), self.lense1)
        pygame.draw.line(self.screen, lense1_arrow_color, (self.lense1.x - 10, self.lense1.y + 10), (self.lense1.x, self.lense1.y), 4)
        pygame.draw.line(self.screen, lense1_arrow_color, (self.lense1.x + 10, self.lense1.y + 10), (self.lense1.x, self.lense1.y), 4)
        pygame.draw.line(self.screen, lense1_arrow_color, (self.lense1.x - 10, self.lense1.y + 600 - 10), (self.lense1.x, self.lense1.y + 600), 4)
        pygame.draw.line(self.screen, lense1_arrow_color, (self.lense1.x + 10, self.lense1.y + 600 - 10), (self.lense1.x, self.lense1.y + 600), 4)
        

        pygame.display.flip()

    def run(self):
        while self.running:
            self.events()
            self.update()
            self.render()


game = Game()
game.run()
