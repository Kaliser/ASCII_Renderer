import numpy as np

class Octahedron:
    def __init__(self, center, size):
        c = np.array(center)
        s = size / 2

        # Define the vertices of the octahedron
        self.vertices = np.array([
            c + [0, 0, s],    # Top vertex
            c + [s, 0, 0],    # Middle vertices
            c + [0, s, 0],
            c + [-s, 0, 0],
            c + [0, -s, 0],
            c + [0, 0, -s]    # Bottom vertex
        ])

        # Define the edges connecting the vertices
        self.edges = [
            (0, 1), (0, 2), (0, 3), (0, 4),  # Top pyramid
            (5, 1), (5, 2), (5, 3), (5, 4),  # Bottom pyramid
            (1, 2), (2, 3), (3, 4), (4, 1)   # Middle square
        ]
