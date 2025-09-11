# colors.py

# Grays (light → dark)
LIGHT_GRAY = (220, 220, 220)
GRAY = (128, 128, 128)
DARK_GRAY = (50, 50, 50)

# Blues (light → dark)
LIGHT_BLUE = (173, 216, 230)  # sky blue
BLUE = (0, 0, 255)            # pure blue
DARK_BLUE = (0, 0, 139)       # navy

# Reds (light → dark)
LIGHT_RED = (255, 182, 193)   # light pinkish red
RED = (255, 0, 0)             # pure red
DARK_RED = (139, 0, 0)        # dark crimson

def grayscale(t):
    v = int(t * 255)
    return (v, v, v)

def fire(t):
    # dark red → orange → yellow → white
    r = int(min(255, t * 3 * 255))
    g = int(min(255, t * 2 * 255))
    b = int(min(255, t * 0.5 * 255))
    return (r, g, b)

def ocean(t):
    # deep blue → cyan → white
    r = int(t * 100)
    g = int(t * 180)
    b = int(150 + t * 105)
    return (r, g, min(255, b))

def psychedelic(t):
    # crazy rainbow using sine waves
    import math
    r = int((math.sin(6.28 * t) + 1) * 127)
    g = int((math.sin(6.28 * t + 2) + 1) * 127)
    b = int((math.sin(6.28 * t + 4) + 1) * 127)
    return (r, g, b)

PALETTES = {
    "grayscale": grayscale,
    "fire": fire,
    "ocean": ocean,
    "psychedelic": psychedelic,
}