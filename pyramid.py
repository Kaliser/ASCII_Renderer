import numpy as np

class Pyramid:
    def __init__(self, center, size):
        c = np.array(center)
        h = size  # Height of the pyramid
        s = size / 2  # Half the base size

        # Define the vertices of the pyramid
        self.vertices = np.array([
            c + [-s, -s, 0],  # Base corner 1
            c + [s, -s, 0],   # Base corner 2
            c + [s, s, 0],    # Base corner 3
            c + [-s, s, 0],   # Base corner 4
            c + [0, 0, h]     # Apex
        ])

        # Define the edges connecting the vertices
        self.edges = [
            (0, 1), (1, 2), (2, 3), (3, 0),  # Base square
            (0, 4), (1, 4), (2, 4), (3, 4)   # Sides
        ]
