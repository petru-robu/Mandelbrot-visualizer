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
    vp: Viewport = field(default_factory = lambda: Viewport(1000, 1000, 3.5, -0.75))
    mandel: MandelbrotSet = field(default_factory = lambda: MandelbrotSet(max_iterations=20, escape_radius=200))
    
    history: list = field(default_factory = lambda: list())
    mandel_surface_idx: int = -1

    def process_viewport(self):
        self.mandel_surface = pygame.Surface((self.vp.vp_width, self.vp.vp_height))
        for y in range(self.vp.vp_height):
            for x in range(self.vp.vp_width):
                c = self.vp.translate_position(x, y)
                instab = self.mandel.stability(c, True)
                grayscale_val = int(instab * 255)
                color = (grayscale_val, grayscale_val, grayscale_val)
                self.mandel_surface.set_at((x, y), color)

        self.mandel_surface_idx += 1
        self.mandel_surface_history.append(self.mandel_surface)
        
        

    def render_mandel(self):
        self.screen.blit(self.mandel_surface_history[self.mandel_surface_idx], (0, 0))

    def run(self):
        selecting = None
        current_rect = None
        ext_square = None

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # left click
                    selecting = True
                    start_pos = event.pos
                    current_rect = pygame.Rect(start_pos, (0, 0))

                elif event.type == pygame.MOUSEMOTION and selecting: 
                    end_pos = event.pos
                    x, y = start_pos
                    w = end_pos[0] - x
                    h = end_pos[1] - y
                    current_rect = pygame.Rect(x, y, w, h)
                    current_rect.normalize()

                    size = min(current_rect.width, current_rect.height)
                    current_rect.width = size
                    current_rect.height = size

                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:  # release
                    selecting = False
                    if current_rect:
                        print("Selected rectangle:", current_rect)
                        print("Changing Viewport!")

                        x, y, w, h = current_rect

                        cpx, cpy = x + w//2, y + h//2
                        center_nmb = self.vp.translate_position(cpx, cpy)
                        world_width = (w) * self.vp.scale

                        self.vp = Viewport(1000, 1000, world_width, center_nmb)
                        self.mandel.max_iterations = int(50 / self.vp.world_width)
                        self.process_viewport()        
            
            self.ui.update(self.vp)

            self.screen.fill("black")

            self.render_mandel()

            self.ui.render()

            if selecting and current_rect:
                s = pygame.Surface((current_rect.width, current_rect.height), pygame.SRCALPHA)
                s.fill((50, 50, 50, 100))
                self.screen.blit(s, current_rect.topleft)
                pygame.draw.rect(self.screen, (80, 80, 80), current_rect, 2)

            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()

g = Game()
g.process_viewport()
g.run()