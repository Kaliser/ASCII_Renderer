import numpy as np

class Cube:
    def __init__(self, center, size):
        c = center
        s = size / 2
        # Define the 8 vertices of the cube
        self.vertices = np.array([
            [c[0] - s, c[1] - s, c[2] - s],
            [c[0] + s, c[1] - s, c[2] - s],
            [c[0] + s, c[1] + s, c[2] - s],
            [c[0] - s, c[1] + s, c[2] - s],
            [c[0] - s, c[1] - s, c[2] + s],
            [c[0] + s, c[1] - s, c[2] + s],
            [c[0] + s, c[1] + s, c[2] + s],
            [c[0] - s, c[1] + s, c[2] + s],
        ])
        # Define the edges connecting the vertices
        self.edges = [
            (0,1), (1,2), (2,3), (3,0),  # Bottom square
            (4,5), (5,6), (6,7), (7,4),  # Top square
            (0,4), (1,5), (2,6), (3,7)   # Vertical edges
        ]
        self.faces = [
            (0, 1, 2, 3),  # Front face
            (4, 5, 6, 7),  # Back face
            (0, 1, 5, 4),  # Bottom face
            (2, 3, 7, 6),  # Top face
            (0, 3, 7, 4),  # Left face
            (1, 2, 6, 5),  # Right face
        ]
    def rotate(self, rotation_matrix):
        """Apply rotation to all vertices."""
        self.vertices = np.dot(self.vertices, rotation_matrix)
