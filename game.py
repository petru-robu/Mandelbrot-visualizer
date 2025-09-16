# game.py
from dataclasses import dataclass, field
import pygame

import numpy as np
from numba import njit

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

        self.help_text1 = self.font.render("Press '[' and ']' to browse history    Press 1-4 to change between color themes (only at the beginning)", True, colors.GRAY)
        self.help_text1_rect = self.help_text1.get_rect()
        self.help_text1_rect.x, self.help_text1_rect.y = 245, 970

        self.info = self.font.render('Made by Petru 11.09.2025', True, colors.GRAY)
        self.info_rect = self.info.get_rect()
        self.info_rect.x, self.info_rect.y = 20, 970

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
        self.screen.blit(self.help_text1, self.help_text1_rect)
        self.screen.blit(self.info, self.info_rect)
        pygame.draw.rect(self.screen, colors.DARK_GRAY, self.vertical_axis_rect)
        pygame.draw.rect(self.screen, colors.DARK_GRAY, self.horizontal_axis_rect)

@dataclass
class Snapshot:
    vp: Viewport
    mandel: MandelbrotSet
    mandel_surface: pygame.Surface

    def __init__(self, vp, mandel, mandel_surface):
        self.vp = vp
        self.mandel = mandel
        self.mandel_surface = mandel_surface
        
@dataclass
class History:
    snapshots: list = field(default_factory=list)
    curr_idx: int = -1

    def add_snapshot(self, snap: Snapshot):
        if self.curr_idx < len(self.snapshots) - 1:
            self.snapshots = self.snapshots[:self.curr_idx+1]

        self.snapshots.append(snap)
        self.curr_idx = len(self.snapshots) - 1

    def get_snapshot(self, idx: int) -> Snapshot:
        if 0 <= idx < len(self.snapshots):
            return self.snapshots[idx]

    def get_next(self) -> Snapshot:
        if self.curr_idx < len(self.snapshots) - 1:
            self.curr_idx += 1
            return self.snapshots[self.curr_idx]
        return None

    def get_previous(self) -> Snapshot:
        if self.curr_idx > 0:
            self.curr_idx -= 1
            return self.snapshots[self.curr_idx]
        return None

@dataclass
class Game:
    screen: pygame.Surface = pygame.display.set_mode((1000, 1000))
    clock: pygame.time.Clock = pygame.time.Clock()
    ui: UI = UI(screen)

    vp: Viewport = field(default_factory = lambda: Viewport(1000, 1000, 3.5, -0.75))
    mandel: MandelbrotSet = field(default_factory = lambda: MandelbrotSet(max_iterations=50, escape_radius=200))
    
    history: History = field(default_factory = lambda: History())

    palette_name: str = 'fire'
    
    def process_viewport(self):
        self.mandel_surface = pygame.Surface((self.vp.vp_width, self.vp.vp_height))
        palette_fn = colors.PALETTES[self.palette_name]

        for y in range(self.vp.vp_height):
            for x in range(self.vp.vp_width):
                c = self.vp.translate_position(x, y)
                instab = self.mandel.stability(c, True)
                color = palette_fn(instab)
                
                self.mandel_surface.set_at((x, y), color)


    def render_mandel(self):
        self.screen.blit(self.mandel_surface, (0, 0))

    def apply_snapshot(self, snap:Snapshot):
        self.vp = snap.vp
        self.mandel = snap.mandel
        self.mandel_surface = snap.mandel_surface

    def run(self):
        selecting = None
        current_rect = None

        self.process_viewport()
        self.history.add_snapshot(Snapshot(self.vp, self.mandel, self.mandel_surface))

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_LEFTBRACKET:
                        prev_snap = self.history.get_previous()
                        if prev_snap:
                            self.apply_snapshot(prev_snap)
                    elif event.key == pygame.K_RIGHTBRACKET:
                        next_snap = self.history.get_next()
                        if next_snap:
                            self.apply_snapshot(next_snap)
                    elif event.key == pygame.K_1:
                        if self.history.curr_idx == 0:
                            self.palette_name = "grayscale"
                            self.vp = Viewport(1000, 1000, 3.5, -0.75)
                            self.mandel = MandelbrotSet(max_iterations=50, escape_radius=200)
                            self.process_viewport()
                            self.history.snapshots[0].mandel_surface = self.mandel_surface
                            self.history.snapshots = self.history.snapshots[:1]
                    elif event.key == pygame.K_2:
                        if self.history.curr_idx == 0:
                            self.palette_name = "fire"
                            self.vp = Viewport(1000, 1000, 3.5, -0.75)
                            self.mandel = MandelbrotSet(max_iterations=50, escape_radius=200)
                            self.process_viewport()
                            self.history.snapshots[0].mandel_surface = self.mandel_surface
                            self.history.snapshots = self.history.snapshots[:1]
                    elif event.key == pygame.K_3:
                        if self.history.curr_idx == 0:
                            self.palette_name = "ocean"
                            self.vp = Viewport(1000, 1000, 3.5, -0.75)
                            self.mandel = MandelbrotSet(max_iterations=50, escape_radius=200)
                            self.process_viewport()
                            self.history.snapshots[0].mandel_surface = self.mandel_surface
                            self.history.snapshots = self.history.snapshots[:1]
                    elif event.key == pygame.K_4:
                        if self.history.curr_idx == 0:
                            self.palette_name = "psychedelic"
                            self.vp = Viewport(1000, 1000, 3.5, -0.75)
                            self.mandel = MandelbrotSet(max_iterations=50, escape_radius=200)
                            self.process_viewport()
                            self.history.snapshots[0].mandel_surface = self.mandel_surface
                            self.history.snapshots = self.history.snapshots[:1]

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
                        x, y, w, h = current_rect

                        cpx, cpy = x + w//2, y + h//2
                        center_nmb = self.vp.translate_position(cpx, cpy)
                        world_width = (w) * self.vp.scale

                        self.vp = Viewport(1000, 1000, world_width, center_nmb)
                        self.mandel.max_iterations = int(75 / self.vp.world_width)

                        self.process_viewport()        
                        self.history.add_snapshot(Snapshot(self.vp, self.mandel, self.mandel_surface))
            
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


def main():
    g = Game()
    g.run()

if __name__ == "__main__":
    main()