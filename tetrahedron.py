import numpy as np

class Tetrahedron:
    def __init__(self, center, size):
        c = np.array(center)
        s = size / np.sqrt(2)

        # Define the vertices of the tetrahedron
        self.vertices = np.array([
            c + [s, s, s],
            c + [-s, -s, s],
            c + [-s, s, -s],
            c + [s, -s, -s]
        ])

        # Define the edges connecting the vertices
        self.edges = [
            (0, 1), (1, 2), (2, 0),  # Base triangle
            (0, 3), (1, 3), (2, 3)   # Sides
        ]
