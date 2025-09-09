# image.py
from dataclasses import dataclass, field
from PIL import Image, ImageEnhance

from mandelbrot import MandelbrotSet
from viewport import Viewport

BLACK_AND_WHITE = '1'
GRAYSCALE = 'L'

@dataclass
class DrawImage:
    image: Image =  field(default_factory = lambda: Image.new(mode=GRAYSCALE, size=(1000, 1000)))
    vp: Viewport = field(default_factory = lambda: Viewport(1000, 1000, 3.5, -0.75))
    mandel: MandelbrotSet = field(default_factory = lambda: MandelbrotSet(max_iterations=20, escape_radius=1000))

    def draw_image(self):
        for y in range(self.vp.vp_height):
            for x in range(self.vp.vp_width):
                c = self.vp.translate_position(x, y)
                instab = 1 - self.mandel.stability(c, True)
                self.image.putpixel((x,y), int(instab*255))

    def show_image(self):  
        #enhancer = ImageEnhance.Brightness(self.image)
        #enhancer.enhance(1.25).show()
        self.image.show()

di = DrawImage()
di.draw_image()
di.show_image()