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
        pygame.display.set_caption("Lenses model")
        self.clock = pygame.time.Clock()

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
        
        self.lense2_x = 800
        self.lense2_selected = 0

        self.scale = 1
        
        self.update_objects()

    def update_objects(self):
        self.object = pygame.rect.Rect(self.object_x, 720 / 2 - 1 - METR * self.object_h, 3, METR * self.object_h)
        self.lense1 = pygame.rect.Rect(self.lense1_x, 720 / 2 - 1 - 300, 3, 600)
        self.lense2 = pygame.rect.Rect(self.lense2_x, 720 / 2 - 1 - 300, 3, 600)

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
                        
                    if self.lense2.collidepoint(*event.pos):
                        self.lense2_selected = not self.lense2_selected

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
        self.clock.tick(60)
        try:
            if self.boxes[0].value:
                self.object_h = float(self.boxes[0].value)
            else:
                self.object_h = 0
        except Exception:
            self.boxes[0].value = "1"
            self.object_h = 1

        if self.object_selected:
            self.object_x = pygame.mouse.get_pos()[0] if pygame.mouse.get_pos()[0] < self.lense1_x else self.object_x
        if self.lense1_selected:
            self.lense1_x = pygame.mouse.get_pos()[0] if self.lense2_x > pygame.mouse.get_pos()[0] > self.object_x  else self.lense1_x
        if self.lense2_selected:
            self.lense2_x = pygame.mouse.get_pos()[0] if pygame.mouse.get_pos()[0] > self.lense1_x else self.lense2_x
            
        if self.boxes[1].value and self.boxes[1].value != "0":
            self.F1_1 = self.lense1_x - float(self.boxes[1].value) * METR
            self.F1_2 = self.lense1_x + float(self.boxes[1].value) * METR
        else:
            self.F1_1 = self.lense1_x - float(1) * METR
            self.F1_2 = self.lense1_x + float(1) * METR
        if self.boxes[2].value and self.boxes[2].value != "0":
            self.F2_1 = self.lense2_x - float(self.boxes[2].value) * METR
            self.F2_2 = self.lense2_x + float(self.boxes[2].value) * METR
        else:
            self.F2_1 = self.lense2_x - float(1) * METR
            self.F2_2 = self.lense2_x + float(1) * METR
        
        first_ray_k = (self.object.y - 360) / (self.lense1.x - self.F1_2)
        first_ray_m = self.object.y - first_ray_k * self.lense1.x
        second_ray_k = (self.object.y - 360) / (self.object.x - self.lense1.x)
        second_ray_m = self.object.y - second_ray_k * self.object_x
        try:
            self.cross_x1 = (second_ray_m - first_ray_m) / (first_ray_k - second_ray_k)
            self.cross_y1 = first_ray_k * self.cross_x1 + first_ray_m
        except Exception:
            pass
        
        if self.cross_x1 < self.lense2_x:
            frk = (self.cross_y1 - 360) / (self.lense2_x - self.F2_2) 
            frm = self.cross_y1 - frk * self.lense2_x
            srk = (self.cross_y1 - 360) / (self.cross_x1 - self.lense2_x)
            srm = self.cross_y1 - srk * self.cross_x1
        else:
            frk = (self.cross_y1 - 360) / (self.cross_x1 - self.F2_1) 
            frm = self.cross_y1 - frk * self.cross_x1
            srk = (self.cross_y1 - 360) / (self.cross_x1 - self.F2_1)
            srm = self.cross_y1 - srk * self.cross_x1
        
        try:
            self.cross_x2 = (srm - frm) / (frk - srk)
            self.cross_y2 = frk * self.cross_x2 + frm
        except Exception:
            pass
        
        self.update_objects()
        
    def do_arrow(self, start_pos, end_pos, y):
        pygame.draw.line(self.screen, BLACK, (start_pos, y), (end_pos, y), 4)
        
        pygame.draw.line(self.screen, BLACK, (start_pos, y), (start_pos + 10, y - 10), 4)
        pygame.draw.line(self.screen, BLACK, (start_pos, y + 1), (start_pos + 10, y + 11), 4)
        
        pygame.draw.line(self.screen, BLACK, (end_pos - 10, y - 10), (end_pos, y), 4)
        pygame.draw.line(self.screen, BLACK, (end_pos - 10, y + 11), (end_pos, y + 1), 4)

        

    def render(self):
        self.screen.fill(GRAY)
        self.print_text(10, 20, "H, m = ", font_size=20)
        self.print_text(10, 70, "F1, m = ", font_size=20)
        self.print_text(10, 120, "F2, m = ", font_size=20)

        for tib in self.boxes:
            self.screen.blit(tib.screen, (tib.rect.x, tib.rect.y))

        pygame.draw.line(self.screen, BLACK, (0, 720 / 2 - 1), (1280, 720 / 2 - 1), 2)
        
        #draw system
        #draw object
        pygame.draw.rect(self.screen, object_arrow_color := (GREEN if self.object_selected else BLACK), self.object)
        pygame.draw.line(self.screen, object_arrow_color, (self.object.x - 10, self.object.y + 10), (self.object.x, self.object.y), 4)
        pygame.draw.line(self.screen, object_arrow_color, (self.object.x + 10, self.object.y + 10), (self.object.x, self.object.y), 4)
        for i in range(10):
            pygame.draw.line(self.screen, BLACK, (self.object_x + 1, 360 + 20 * i), (self.object_x + 1, 360 + 20 * i + 10), 3)
        
        self.print_text(self.object.x + 20, self.object.y + self.object.height / 2, message="H")
        
        # draw lenses
        pygame.draw.rect(self.screen, lense1_arrow_color := (GREEN if self.lense1_selected else BLACK), self.lense1)
        pygame.draw.line(self.screen, lense1_arrow_color, (self.lense1.x - 10, self.lense1.y + 10), (self.lense1.x, self.lense1.y), 4)
        pygame.draw.line(self.screen, lense1_arrow_color, (self.lense1.x + 10, self.lense1.y + 10), (self.lense1.x, self.lense1.y), 4)
        pygame.draw.line(self.screen, lense1_arrow_color, (self.lense1.x - 10, self.lense1.y + 600 - 10), (self.lense1.x, self.lense1.y + 600), 4)
        pygame.draw.line(self.screen, lense1_arrow_color, (self.lense1.x + 10, self.lense1.y + 600 - 10), (self.lense1.x, self.lense1.y + 600), 4)
        
        pygame.draw.rect(self.screen, lense2_arrow_color := (GREEN if self.lense2_selected else BLACK), self.lense2)
        pygame.draw.line(self.screen, lense2_arrow_color, (self.lense2.x - 10, self.lense2.y + 10), (self.lense2.x, self.lense2.y), 4)
        pygame.draw.line(self.screen, lense2_arrow_color, (self.lense2.x + 10, self.lense2.y + 10), (self.lense2.x, self.lense2.y), 4)
        pygame.draw.line(self.screen, lense2_arrow_color, (self.lense2.x - 10, self.lense2.y + 600 - 10), (self.lense2.x, self.lense2.y + 600), 4)
        pygame.draw.line(self.screen, lense2_arrow_color, (self.lense2.x + 10, self.lense2.y + 600 - 10), (self.lense2.x, self.lense2.y + 600), 4)
        
        #draw len lines
        self.do_arrow(self.object_x, self.lense1_x, 720 / 2 + 30)
        delta = self.lense1_x - self.object_x
        self.print_text(self.object_x + (delta) / 2 - 10 * len(str(delta)) - 10, 360 + 5, f"d1 = {round(delta / METR, 2)}м")
        delta = self.lense2_x - self.object_x
        self.do_arrow(self.object_x, self.lense2_x, 360 + 70)
        self.print_text(self.object_x + (delta) / 2 - 10 * len(str(delta)) - 10, 360 + 45, f"d2 = {round(delta / METR, 2)}м")
        
        #draw rays and focus dots
        #point F1
        pygame.draw.circle(self.screen, BLACK, (self.F1_1, 360), 4)
        self.print_text(self.F1_1, 335, "F1")
        pygame.draw.circle(self.screen, BLACK, (self.F1_2, 360), 4)
        self.print_text(self.F1_2, 335, "F1")
        
        #point F2
        pygame.draw.circle(self.screen, BLACK, (self.F2_1, 360), 4)
        self.print_text(self.F2_1, 335, "F2")
        pygame.draw.circle(self.screen, BLACK, (self.F2_2, 360), 4)
        self.print_text(self.F2_2, 335, "F2")
        
        
        #rays
        #ray 1
        pygame.draw.line(self.screen, BLACK, (self.object_x, self.object.y), (self.lense1.x, self.object.y), 1)
        pygame.draw.line(self.screen, BLACK, (self.lense1.x, self.object.y), (self.cross_x1, self.cross_y1), 1)
        pygame.draw.line(self.screen, BLACK, (self.object.x, self.object.y), (self.cross_x1, self.cross_y1), 1)
        
        pygame.draw.line(self.screen, BLACK, (self.cross_x1, self.cross_y1), (self.cross_x1, 360), 3)
        self.print_text(self.cross_x1 + 10, 360 + (self.cross_y1 - 360) / 2, f"h2 = {round((self.cross_y1 - 360) / 100, 2)}")
        
        #ray 2
        try:
            pygame.draw.line(self.screen, BLACK, (self.cross_x1, self.cross_y1), (self.lense2_x, self.cross_y1), 1)
            pygame.draw.line(self.screen, BLACK, (self.lense2_x, self.cross_y1), (self.cross_x2, self.cross_y2), 1)
            pygame.draw.line(self.screen, BLACK, (self.cross_x1, self.cross_y1), (self.cross_x2, self.cross_y2), 1)
            
            pygame.draw.line(self.screen, BLACK, (self.cross_x2, self.cross_y2), (self.cross_x2, 360), 3)
        except Exception:
            pass
            
        
        pygame.display.flip()

    def run(self):
        while self.running:
            self.events()
            self.update()
            self.render()


game = Game()
game.run()
