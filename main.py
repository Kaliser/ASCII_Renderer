import random
import numpy as np
import time
import os
import math
from cube import Cube
from donut import Donut
from figure8 import Figure8
from pyramid import Pyramid
from sphere import Sphere
from tetrahedron import Tetrahedron
from octahedron import Octahedron

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
        os.system('cls' if os.name == 'nt' else 'clear')
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



def project_vertex(vertex, screen_width, screen_height, scale=4, offset=(20,-20)):
    """
    Project a 3D vertex onto 2D screen coordinates using orthographic projection.
    """
    x, y, z = vertex
    # orthographic projection: ignore z-coordinate
    x_proj = x * scale + offset[0]
    y_proj = y * scale + offset[1]
    # invert y-axis for correct display
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
    # rotation around X-axis
    cos_x, sin_x = math.cos(angle_x), math.sin(angle_x)
    y, z = y * cos_x - z * sin_x, y * sin_x + z * cos_x
    # rotation around Y-axis
    cos_y, sin_y = math.cos(angle_y), math.sin(angle_y)
    x, z = x * cos_y + z * sin_y, -x * sin_y + z * cos_y
    # rotation around Z-axis
    cos_z, sin_z = math.cos(angle_z), math.sin(angle_z)
    x, y = x * cos_z - y * sin_z, x * sin_z + y * cos_z
    return (x, y, z)

def draw_face(canvas, points, char):
    num_points = len(points)
    for i in range(num_points):
        x0, y0 = points[i]
        x1, y1 = points[(i + 1) % num_points]
        canvas.draw_line(x0, y0, x1, y1, char=char)

def fill_polygon(canvas, vertices, char):
    """
    Fill a polygon on the canvas given its vertices and fill character.
    Uses the Scanline Fill Algorithm.
    """
    # extract x and y coordinates from vertices
    x_coords = [int(round(x)) for x, y in vertices]
    y_coords = [int(round(y)) for x, y in vertices]
    num_vertices = len(vertices)

    # find the bounding box of the polygon
    min_y = max(min(y_coords), 0)
    max_y = min(max(y_coords), canvas.height - 1)

    # create an edge table
    edge_table = []
    for i in range(num_vertices):
        x0, y0 = x_coords[i], y_coords[i]
        x1, y1 = x_coords[(i + 1) % num_vertices], y_coords[(i + 1) % num_vertices]

        if y0 == y1:
            continue  # Ignore horizontal edges

        if y0 > y1:
            x0, y0, x1, y1 = x1, y1, x0, y0  # swap to ensure y0 <= y1

        inverse_slope = (x1 - x0) / (y1 - y0)
        edge_table.append({
            'y_min': y0,
            'y_max': y1,
            'x_at_y_min': x0,
            'inverse_slope': inverse_slope
        })

    # sort the edge table by y_min
    edge_table.sort(key=lambda e: e['y_min'])

    # scanline fill
    y = min_y
    active_edges = []
    while y <= max_y:
        # add edges where y == y_min to active edges
        for edge in edge_table:
            if edge['y_min'] == y:
                active_edges.append(edge)

        # remove edges where y == y_max from active edges
        active_edges = [e for e in active_edges if e['y_max'] != y]

        # sort active edges by x_at_y_min
        active_edges.sort(key=lambda e: e['x_at_y_min'])

       # fill between pairs of intersections
        i = 0
        while i < len(active_edges) - 1:
            x_start = active_edges[i]['x_at_y_min']
            x_end = active_edges[i + 1]['x_at_y_min']

            x_start = int(round(x_start))
            x_end = int(round(x_end))

            # Clip to canvas bounds
            x_start = max(x_start, 0)
            x_end = min(x_end, canvas.width - 1)

            for x in range(x_start, x_end + 1):
                if 0 <= x < canvas.width and 0 <= y < canvas.height:
                    canvas.canvas[y, x] = char
            i += 2  # move to the next pair

        # increment x_at_y_min for each active edge
        for edge in active_edges:
            edge['x_at_y_min'] += edge['inverse_slope']

        y += 1
        
def instantiate_shape(shape_name):
    if shape_name == "cube":
        return Cube(center=(0, 0, 0), size=5)
    elif shape_name == "pyramid":
        return Pyramid(center=(0, 0, 0), size=5)
    elif shape_name == "tetrahedron":
        return Tetrahedron(center=(0, 0, 0), size=5)
    elif shape_name == "octahedron":
        return Octahedron(center=(0, 0, 0), size=5)
    elif shape_name == "sphere":
        return Sphere(center=(0, 0, 0), radius=5, segments=12, rings=12)
    else:
        raise ValueError(f"Invalid shape: {shape_name}")

def main():
    parser = argparse.ArgumentParser(description="Render 3D shapes.")
    parser.add_argument(
        "--shape",
        type=str,
        choices=["cube", "donut", "figure8", "pyramid", "sphere", "tetrahedron", "octahedron"],
        default="cube",
        help="Shape to render.",
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
        default='p',
        help='Projection method (orthographic "o" or perspective "p").',
    )
    parser.add_argument(
        "--mode",
        type=str,
        choices=["wireframe", "solid"],
        default="wireframe",
        help="Rendering mode: 'wireframe' or 'solid'.",
    )
    parser.add_argument(
        "--screensaver",
        action="store_true",
        help="Enable screensaver mode to cycle through different shapes.",
    )
    args = parser.parse_args()
    FRAME_DURATION = 1 / args.fps

    ##### Canvas Dimensions #####
    width = 80
    height = 40
    canvas = ASCIICanvas3D(width, height, background=' ')


    available_shapes = ["cube", "pyramid", "tetrahedron", "octahedron", "sphere", "donut"]

    def instantiate_shape(shape_name):
        if shape_name == "cube":
            return Cube(center=(0, 0, 0), size=5)
        elif shape_name == "donut":
            return Donut(R=3, r=1, segments=30)
        elif shape_name == "figure8":
            return Figure8(center=(0, 0, 0), size=8)
        elif shape_name == "pyramid":
            return Pyramid(center=(0, 0, 0), size=5)
        elif shape_name == "sphere":
            return Sphere(center=(0, 0, 0), radius=4, segments=9, rings=9)
        elif shape_name == "tetrahedron":
            return Tetrahedron(center=(0, 0, 0), size=6)
        elif shape_name == "octahedron":
            return Octahedron(center=(0, 0, 0), size=8)
        else:
            raise ValueError(f"Invalid shape: {shape_name}")

    # screensaver preparation
    current_shape_index = 0
    shape_display_duration = 5  # Duration in seconds
    last_switch_time = time.time()

    # first shape instantiation
    if args.screensaver:
        shape_name = available_shapes[current_shape_index]
        shape = instantiate_shape(shape_name)
    else:
        shape = instantiate_shape(args.shape)

    # rotation angles
    angle_x, angle_y, angle_z = 0, 0, 0
    
    project = project_vertex if args.projection == 'o' else perspective_projection

    ###### Light position ######
    light_position = np.array([0, 20, -30])

    # ASCII characters representing different brightness levels
    ascii_chars = [' ', '.', ':', '-', '=', '+', '*', '#', '%', '@']

    def get_ascii_char(brightness):
        index = int(brightness * (len(ascii_chars) - 1))
        return ascii_chars[index]

    try:
        while True:
            current_time = time.time()
            # check if screensaver mode is enabled and if it's time to switch shapes
            if args.screensaver and (current_time - last_switch_time >= shape_display_duration):
                # wwitch to the next shape
                current_shape_index = (current_shape_index + 1) % len(available_shapes)
                shape_name = available_shapes[current_shape_index]
                shape = instantiate_shape(shape_name)
                last_switch_time = current_time  # Reset the switch time

            canvas.clear()

            # rotate verticesand project them
            rotated_vertices = [rotate_vertex(v, angle_x, angle_y, angle_z) for v in shape.vertices]
            projected_vertices = []
            for vertex in rotated_vertices:
                x, y = project(vertex, width, height)
                projected_vertices.append((x, y))

            if args.mode == 'wireframe':
                # Draw edges
                for edge in shape.edges:
                    start, end = edge
                    x0, y0 = projected_vertices[start]
                    x1, y1 = projected_vertices[end]
                    canvas.draw_line(x0, y0, x1, y1, char='#')
            elif args.mode == 'solid':
                # ensure the shape supports solid rendering
                if not hasattr(shape, 'faces'):
                    print(f"The shape '{shape_name}' does not support solid rendering.")
                    break

                ambient = 0.2 # ambient light level (0 to 1)

                # draw and shade faces
                for face in shape.faces:
                    face_vertices = [rotated_vertices[i] for i in face]

                    # calculate face normal
                    v0, v1, v2 = face_vertices[:3]
                    edge1 = np.array(v1) - np.array(v0)
                    edge2 = np.array(v2) - np.array(v0)
                    normal = np.cross(edge1, edge2)
                    normal = normal / np.linalg.norm(normal)

                    # calculate brightness using the light direction
                    to_light = light_position - np.array(v0)
                    to_light = to_light / np.linalg.norm(to_light)
                    brightness = np.dot(normal, to_light)
                    brightness = max(0, brightness)  # Clamp to [0, 1]

                    # add ambient light component
                    brightness = ambient + (1 - ambient) * brightness
                    brightness = min(1, brightness)  # Ensure brightness does not exceed 1

                    # map brightness to ASCII char
                    char = get_ascii_char(brightness)

                    # project face vertices and fill the face
                    face_projected = [project(v, width, height) for v in face_vertices]
                    fill_polygon(canvas, face_projected, char)

            canvas.display()

            # Update rotation angles
            angle_x += 0.02
            angle_y += 0.02
            angle_z += 0.02

            # frame rate
            time.sleep(FRAME_DURATION)
    except KeyboardInterrupt:
        print("\nRendering stopped.")
    finally:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\033[?25h", end="")

if __name__ == "__main__":
    main()