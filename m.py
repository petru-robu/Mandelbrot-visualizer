import pygame

from math import log
class MandelbrotSet:
    def __init__(self, max_iterations, escape_radius = 2.0):
        self.max_iterations = max_iterations
        self.escape_radius = escape_radius

    def __contains__(self, c: complex) -> bool:
        return self.stability(c) == 1

    def stability(self, c: complex, smooth=False) -> float:
        return self.escape_count(c, smooth) / self.max_iterations

    def escape_count(self, c: complex, smooth=False) -> int | float:
        z = 0
        for iteration in range(self.max_iterations):
            z = z ** 2 + c
            if abs(z) > self.escape_radius:
                if smooth:
                    return iteration + 1 - log(log(abs(z))) / log(2)
                return iteration
        return self.max_iterations

class Viewport:
    def __init__(self, center: complex, world_width: float, view_width: int, view_height: int):
        self.center = center
        self.world_width = world_width
        self.view_width = view_width
        self.view_height = view_height

    @property
    def scale(self):
        return self.world_width / self.view_width

    @property
    def world_height(self):
        return self.scale * self.view_height

    @property
    def offset(self):
        return self.center + complex(-self.world_width, self.world_height) / 2

    def __iter__(self):
        for y in range(self.view_height):
            for x in range(self.view_width):
                yield Pixel(self, x, y)

class Pixel:
    def __init__(self, viewport: Viewport, x:int, y:int):
        self.viewport = viewport
        self.x = x
        self.y = y

    def __complex__(self):
        return (complex(self.x, -self.y) * self.viewport.scale + self.viewport.offset )

class UI:
    def __init__(self, screen, vp):
        self.screen = screen
        self.vp = vp
        self.font = pygame.font.Font('arial.ttf', 20)

        
    def update_mouse_pos_text(self, pos):
        mx, my = pos.real, pos.imag
        mx, my = round(mx, 3), round(my, 3)
        self.mouse_pos_text = self.font.render(f'mouse pos: {mx}, {my}', True, 'red')
        self.mouse_pos_text_rect = self.mouse_pos_text.get_rect()
        self.mouse_pos_text_rect.center = (100, 30)

    def render(self):
        self.screen.blit(self.mouse_pos_text, self.mouse_pos_text_rect)
        


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((1600, 1000))
        self.clock = pygame.time.Clock()

        self.vp = Viewport(-1 + 0j, 4.0, 1000, 1000)
        self.mandelbrot = MandelbrotSet(max_iterations=256, escape_radius=1000)

        self.ui = UI(self.screen, self.vp)

        self.to_render = []

    def change_viewport(self):
        pass

    def update_viewport(self):
        for pixel in self.vp:
            if complex(pixel) in self.mandelbrot:
                self.to_render.append(pixel)

    def run(self):
        self.update_viewport()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # update
            #self.ui.update_mouse_pos_text(pygame.mouse.get_pos())
            #mx, my = pygame.mouse.get_pos()
            #self.ui.update_mouse_pos_text(complex(Pixel(self.vp, mx, my)))

            # render
            self.screen.fill("black")

            for pixel in self.to_render:
                self.screen.set_at((pixel.x, pixel.y), 'blue')

            pygame.draw.rect(self.screen, 'red', pygame.Rect(800, 0, 1, 1000 ))

            #self.ui.render()
            
            # update frame
            pygame.display.flip()
            self.clock.tick(60) # limit fps to 60

        pygame.quit()
    


pygame.init()
game = Game()
game.run()



        