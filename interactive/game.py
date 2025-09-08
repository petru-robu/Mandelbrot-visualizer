# game.py
from dataclasses import dataclass, field
import pygame

from mandelbrot import MandelbrotSet
from viewport import Viewport
import colors

pygame.init()

class UI:
    def __init__(self, screen: pygame.Surface):
        self.font = pygame.font.Font('arial.ttf', 16)
        self.screen = screen

        W, H = self.screen.get_size()
        print(W, H)
        self.vertical_axis_rect = pygame.Rect(W//2, 0, 1, H)
        self.horizontal_axis_rect = pygame.Rect(0, H//2, W, 1)

    def update(self, vp:Viewport):
        mx, my = pygame.mouse.get_pos()
        self.mouse_pos_text = self.font.render(f'mp: {mx}, {my}', True, colors.GRAY)
        self.mouse_pos_text_rect = self.mouse_pos_text.get_rect()
        self.mouse_pos_text_rect.center = (62, 25)

        nmb_pos = vp.translate_position(mx, my)
        re, im = round(nmb_pos.real, 3), round(nmb_pos.imag, 3)
        nmb_pos = complex(re, im)

        self.nmb_pos_text = self.font.render(f'wp: {nmb_pos}', True, colors.GRAY)
        self.nmb_pos_text_rect = self.mouse_pos_text.get_rect()
        self.nmb_pos_text_rect.center = (62, 50)

    def render(self):
        self.screen.blit(self.mouse_pos_text, self.mouse_pos_text_rect)
        self.screen.blit(self.nmb_pos_text, self.nmb_pos_text_rect)
        pygame.draw.rect(self.screen, colors.DARK_GRAY, self.vertical_axis_rect)
        pygame.draw.rect(self.screen, colors.DARK_GRAY, self.horizontal_axis_rect)

@dataclass
class Game:
    screen: pygame.Surface = pygame.display.set_mode((1000, 1000))
    clock: pygame.time.Clock = pygame.time.Clock()
    ui: UI = UI(screen)
    vp: Viewport = field(default_factory = lambda: Viewport(1000, 1000, 0.002, -0.7435 + 0.1314j))
    mandel: MandelbrotSet = field(default_factory = lambda: MandelbrotSet(100))


    def init(self):
        pass

    def calculate_mandelbrot(self):
        self.mandel_render = []
        for y in range(self.vp.vp_height):
            for x in range(self.vp.vp_width):
                c = self.vp.translate_position(x, y)
                if c in self.mandel:
                    self.mandel_render.append((x, y))

    def render_mandel(self):
        for pixel in self.mandel_render:
                self.screen.set_at(pixel, colors.LIGHT_BLUE)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

            self.ui.update(self.vp)

            self.screen.fill("black")

            self.render_mandel()

            self.ui.render()

            pygame.display.flip()
            self.clock.tick(30)
        pygame.quit()

g = Game()
g.calculate_mandelbrot()
g.run()