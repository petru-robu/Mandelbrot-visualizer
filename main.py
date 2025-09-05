import pygame

def test_convergence(c: complex, max_iter: int, min_val_diverg: int):
    z = 0 + 0j
    for i in range(max_iter):
        if abs(z) > min_val_diverg:
            return i # diverges
        z = z * z + c
    return max_iter # converges


def in_mandelbrot(c: complex):
    max_iter = 100
    if test_convergence(c, max_iter, 2) != max_iter:
        return False
    return True


def translate(value, fromMin, fromMax, toMin, toMax):
    # Figure out how 'wide' each range is
    fromSpan = fromMax - fromMin
    toSpan = toMax - toMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - fromMin) / float(fromSpan)

    # Convert the 0-1 range into a value in the right range.
    return round(toMin + (valueScaled * toSpan), 3)

def convert_int_range(fromMin, fromMax, toMin, toMax):
    new_range = []
    for nmb in range(fromMin, fromMax):
        new_range.append(round(translate(nmb, fromMin, fromMax, toMin, toMax),4))
    return new_range


class Plotter:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen

    def plot_point(self, x: int, y: int, color: pygame.Color = 'blue'):
        self.screen.set_at((x,y), color)


screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
plt = Plotter(screen)

xmin, xmax= -0.5, 0.5
ymin, ymax = -0.5, 0.5

start_x, start_y, end_x, end_y = 100, 100, 800, 800

#print(convert_int_range(100, 200, xmin, xmax))

map = {}
for px in range(start_x, end_x):
    for py in range(start_y, end_y):
        map[(px, py)] = translate(px, start_x, end_x, xmin, xmax) + translate(py, start_y, end_y, ymin, ymax) * 1j

#print(map)


points_to_plot = set()
for point in map:
    if in_mandelbrot(map[point]):
        points_to_plot.add(point)


running = True
while running:
    # poll for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill screen
    screen.fill("black")

    for point in points_to_plot:
        plt.plot_point(*point)
    
    # update frame
    pygame.display.flip()
    clock.tick(60) # limit fps to 60

pygame.quit()





