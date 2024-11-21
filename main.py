import numpy as np
import time
import os
import math
from cube import Cube
from donut import Donut
import argparse

class ASCIICanvas3D:
    def __init__(self, width, height, background=' '):
        self.width = width
        self.height = height
        self.background = background
        self.canvas = np.full((height, width), background, dtype='<U1')
    
    def clear(self):
        self.canvas[:] = self.background
    
    def display(self):
        # Clear the screen
        os.system('cls' if os.name == 'nt' else 'clear')
        # Print the canvas
        for row in self.canvas:
            print(''.join(row))
    
    def draw_line(self, x0, y0, x1, y1, char='#'):
        """Draw a line from (x0, y0) to (x1, y1) using Bresenham's algorithm."""
        x0 = int(round(x0))
        y0 = int(round(y0))
        x1 = int(round(x1))
        y1 = int(round(y1))
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy
        
        while True:
            if 0 <= x0 < self.width and 0 <= y0 < self.height:
                self.canvas[y0, x0] = char
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy


def rotation_matrix_x(angle):
    """Rotation matrix around the X-axis by the given angle in radians."""
    return np.array([
        [1, 0, 0],
        [0, math.cos(angle), -math.sin(angle)],
        [0, math.sin(angle), math.cos(angle)]
    ])

def rotation_matrix_y(angle):
    """Rotation matrix around the Y-axis by the given angle in radians."""
    return np.array([
        [math.cos(angle), 0, math.sin(angle)],
        [0, 1, 0],
        [-math.sin(angle), 0, math.cos(angle)]
    ])

def rotation_matrix_z(angle):
    """Rotation matrix around the Z-axis by the given angle in radians."""
    return np.array([
        [math.cos(angle), -math.sin(angle), 0],
        [math.sin(angle), math.cos(angle), 0],
        [0, 0, 1]
    ])

def project_vertex(vertex, screen_width, screen_height, scale=4, offset=(20,-20)):
    """
    Project a 3D vertex onto 2D screen coordinates using orthographic projection.
    """
    x, y, z = vertex
    # Orthographic projection: ignore z-coordinate
    x_proj = x * scale + offset[0]
    y_proj = y * scale + offset[1]
    # Invert y-axis for correct display
    y_proj = -y_proj
    return (x_proj, y_proj)

def perspective_projection(vertex, screen_width, screen_height, fov=200, viewer_distance=45):
    """
    Project a 3D vertex onto 2D screen coordinates using perspective projection.
    """
    x, y, z = vertex
    factor = fov / (viewer_distance + z)
    x_proj = x * factor + screen_width / 2
    y_proj = -y * factor + screen_height / 2
    return (x_proj, y_proj)


def rotate_vertex(vertex, angle_x, angle_y, angle_z):
    x, y, z = vertex
    # Rotation around X-axis
    cos_x, sin_x = math.cos(angle_x), math.sin(angle_x)
    y, z = y * cos_x - z * sin_x, y * sin_x + z * cos_x
    # Rotation around Y-axis
    cos_y, sin_y = math.cos(angle_y), math.sin(angle_y)
    x, z = x * cos_y + z * sin_y, -x * sin_y + z * cos_y
    # Rotation around Z-axis
    cos_z, sin_z = math.cos(angle_z), math.sin(angle_z)
    x, y = x * cos_z - y * sin_z, x * sin_z + y * cos_z
    return (x, y, z)


def main():
    parser = argparse.ArgumentParser(description="Render 3D shapes.")
    parser.add_argument(
        "--shape",
        type=str,
        choices=["cube", "donut"],
        default="cube",
        help="Shape to render (cube or donut).",
    )
    parser.add_argument(
        "--fps",
        type=int,
        default=30,
        help="Frames per second.",
    )
    parser.add_argument(
        '--projection',
        type=str,
        choices=['o', 'p'],
        default='perspective',
        help='Projection method (orthographic or perspective) using o or p.',
    )
    args = parser.parse_args()
    FRAME_DURATION = 1 / args.fps

    # Canvas dimensions
    width = 80
    height = 40
    canvas = ASCIICanvas3D(width, height, background=' ')

    # Instantiate shape
    shape = Cube(center=(0, 0, 0), size=5) if args.shape == "cube" else Donut(R=3, r=1, segments=10)

    # Rotation angles
    angle_x, angle_y, angle_z = 0, 0, 0

    # Scaling factor and offset for projection
    scale = 2
    offset = (width // 2, height // 2)

    project = project_vertex if args.projection == 'o' else perspective_projection
    try:
        while True:
            canvas.clear()

            # Rotate vertices
            rotated_vertices = [rotate_vertex(v, angle_x, angle_y, angle_z) for v in shape.vertices]

            # Project vertices
            projected_vertices = []
            for vertex in rotated_vertices:
                x, y = project(vertex, width, height)
                projected_vertices.append((x, y))

            # Draw edges
            for edge in shape.edges:
                start, end = edge
                x0, y0 = projected_vertices[start]
                x1, y1 = projected_vertices[end]
                canvas.draw_line(x0, y0, x1, y1, char='&')

            # Display the canvas
            canvas.display()

            # Update rotation angles
            angle_x += 0.03
            angle_y += 0.02
            angle_z += 0.01

            # Control frame rate
            time.sleep(FRAME_DURATION)
    except KeyboardInterrupt:
        # Exit gracefully on Ctrl+C
        print("\nRendering stopped.")
    finally:
        # Clear the console and show the cursor again
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\033[?25h", end="")  # Show cursor again

if __name__ == "__main__":
    main()