A simple terminal-based 3D renderer that displays various 3D shapes using ASCII characters. The program supports both wireframe and solid rendering modes and allows switching between different shapes.

## Features
- **Renders 3D Shapes**: Cube, Pyramid, Tetrahedron, Octahedron, Sphere, and Donut.
- **Projection Methods**: Orthographic and Perspective.
- **Rendering Modes**: Wireframe and Solid (with shading).
- **Screensaver Mode**: Cycles through different shapes automatically.
- **ASCII Shading**: Uses ASCII characters to simulate lighting effects.

## Installation
### Prerequisites
- Python 3.x
- NumPy


## Usage
Run the program with:
```sh
python main.py [options]
```

### Command-line Arguments:
| Argument       | Description                                         | Default |
|---------------|-----------------------------------------------------|---------|
| `--shape`     | Shape to render (`cube`, `donut`, `pyramid`, `sphere`, `tetrahedron`, `octahedron`). | `cube` |
| `--fps`       | Frames per second.                                 | `30`    |
| `--projection` | Projection method (`o` for orthographic, `p` for perspective). | `p` |
| `--mode`      | Rendering mode (`wireframe` or `solid` (`solid` currently only supported for cubes)).            | `wireframe` |
| `--screensaver` | Enable screensaver mode to cycle through different shapes. | `False` |

### Example Commands:
Render a rotating wireframe cube:
```sh
python main.py --shape cube --mode wireframe
```

Render a solid-shaded sphere with perspective projection:
```sh
python main.py --shape sphere --mode solid --projection p
```

Run in screensaver mode:
```sh
python main.py --screensaver
```

## Controls
- **`CTRL + C`**: Stop the rendering.

## How It Works
1. **3D Shapes**: Defined using vertices and edges, with optional faces for solid rendering.
2. **Projection**: Converts 3D points into 2D screen coordinates.
3. **Rotation**: Uses rotation matrices to animate shapes.
4. **Rendering**:
   - **Wireframe Mode**: Draws edges between vertices.
   - **Solid Mode**: Fills faces using ASCII shading.
5. **Lighting (Solid Mode Only)**:
   - Normal calculation for shading.
   - ASCII brightness mapping based on a light source.

---