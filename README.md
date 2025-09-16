# Interactive Mandelbrot Explorer
An interactive Mandelbrot set explorer built in **Python** with **Pygame** — featuring a *zoom selection*, *history mechanism* to navigate back and forth between zoom levels, *smooth coloring* and *palette switching*.

There is also the possibility of generating an image of the mandelbrot set using **Pillow**. This is separate from the main game window.

Dependency management is handled by **Poetry** for reproducible builds and easy setup.

## Features
### 1. Mandelbrot Set
- Computes the *Mandelbrot set* with adjustable zoom and center.
- Supports *smooth coloring* (based on escape counts) for visually appealing gradients. Removal of banding artifacts when coloring.
- Multiple *color palettes* (grayscale, fire, ocean, psychedelic).

### 2. History Mechanism
- Every zoom creates a *snapshot* of:
  - Viewport (center + zoom level)
  - Mandelbrot parameters
  - Rendered surface
- Navigate through history with:
  - [ = Go to previous snapshot  
  - ] = Go to next snapshot
- Makes it easy to explore deep zooms and return to previous views instantly.

### 3. Speed Optimizations with Numba
- The escape count algorithm is *JIT-compiled with Numba*.
- Performance is several times faster than a pure-Python implementation.
- The use of python *complex* data-type is also avoided as it is slow.

### 4. Poetry Integration
- Reproducible environment and locked dependencies.
- Easy setup on a fresh machine.

## Installation & Running
Clone the repository:
```bash
git clone https://github.com/petru-robu/Mandelbrot-visualizer/
cd Mandelbrot-visualizer
```

Install dependencies using Poetry:
```bash
poetry install
```

Run the Mandelbrot explorer:
```bash
poetry run mandelbrot
```

## Controls
Key / Action	Description:
- Left Click + Drag - Select a zoom area
- [	- Go back to previous snapshot
- ]	- Go forward to next snapshot
- 1/2/3/4 - Switch to grayscale/fire/ocean/psychedelic color palette
- ESC	- Quit program

## Project Structure
```
├── colors.py        # File that contains hard-coded colors and color pallettes
├── game.py          # Main entry point with Game class and event loop
├── viewport.py      # Viewport class for pixel-to-complex mapping
├── mandelbrot.py    # MandelbrotSet class, with Numba-accelerated computations
└── image.py         # Functions for plotting the Mandelbrot set as an image file.
```

## Tech Stack
Python 3.10+
Pygame – for rendering and user interaction
NumPy – for array-based computations
Numba – for JIT acceleration of Mandelbrot calculations
Poetry – for dependency and environment management


## Future Improvements
- Fully vectorize drawing functions to eliminate Python loops and speed up rendering.
- Add saving and loading of favorite views as JSON snapshots.

## License
MIT License — feel free to use, modify, and redistribute this project.
