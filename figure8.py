import numpy as np
from rotate import rotation_matrix_x, rotation_matrix_y, rotation_matrix_z

class Figure8:
    def __init__(self, center, size, segments=16):
        self.center = np.array(center)
        self.size = size
        self.segments = segments  # Number of segments to approximate the loops

        # Generate vertices for the figure-eight shape
        self.vertices = []
        self.edges = []
        self.faces = []

        # Parameters for the loops
        r = size / 4  # Radius of the loops
        d = size / 2  # Distance from the center to the loop centers

        # Generate vertices for the upper loop
        for i in range(segments):
            theta = 2 * np.pi * i / segments
            x = self.center[0] + d + r * np.cos(theta)
            y = self.center[1] + r * np.sin(theta)
            z = self.center[2]
            self.vertices.append([x, y, z])

        # Generate vertices for the lower loop
        offset = len(self.vertices)
        for i in range(segments):
            theta = 2 * np.pi * i / segments
            x = self.center[0] - d + r * np.cos(theta)
            y = self.center[1] + r * np.sin(theta)
            z = self.center[2]
            self.vertices.append([x, y, z])

        # Convert vertices to NumPy array
        self.vertices = np.array(self.vertices)

        # Create edges for upper and lower loops
        for i in range(segments):
            # Upper loop edges
            self.edges.append((i, (i + 1) % segments))
            # Lower loop edges
            self.edges.append((offset + i, offset + (i + 1) % segments))

            # Faces for upper loop
            next_i = (i + 1) % segments
            self.faces.append((i, next_i, offset + next_i, offset + i))

        # Connect the loops
        for i in range(segments):
            self.edges.append((i, offset + i))

        # Faces connecting the loops
        for i in range(segments):
            next_i = (i + 1) % segments
            self.faces.append((i, next_i, offset + next_i, offset + i))

    def rotate(self, angle_x, angle_y, angle_z):
        """Rotate all vertices around the center by given angles."""
        rotation_x = rotation_matrix_x(angle_x)
        rotation_y = rotation_matrix_y(angle_y)
        rotation_z = rotation_matrix_z(angle_z)

        rotation_matrix = rotation_z @ rotation_y @ rotation_x

        self.vertices = np.dot(self.vertices - self.center, rotation_matrix.T) + self.center
