import numpy as np

class Sphere:
    def __init__(self, center, radius, segments=12, rings=12):
        c = np.array(center)
        self.vertices = []
        self.edges = []

        # Generate vertices
        for i in range(rings + 1):
            theta = np.pi * i / rings  # From 0 to pi
            sin_theta = np.sin(theta)
            cos_theta = np.cos(theta)

            for j in range(segments):
                phi = 2 * np.pi * j / segments  # From 0 to 2pi
                sin_phi = np.sin(phi)
                cos_phi = np.cos(phi)

                x = c[0] + radius * sin_theta * cos_phi
                y = c[1] + radius * sin_theta * sin_phi
                z = c[2] + radius * cos_theta

                self.vertices.append([x, y, z])

        # Generate edges
        for i in range(rings):
            for j in range(segments):
                current = i * segments + j
                next_segment = current + 1 if (j + 1) % segments else current + 1 - segments
                next_ring = current + segments

                if next_ring < len(self.vertices):
                    self.edges.append((current, next_ring))
                self.edges.append((current, next_segment))

    