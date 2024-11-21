import math

class Donut:
    def __init__(self, R=10, r=3, segments=30):
        self.vertices = []
        self.edges = []
        self.R = R  # major radius
        self.r = r  # minor radius
        self.segments = segments
        self.generate_vertices()
        self.generate_edges()

    def generate_vertices(self):
        for i in range(self.segments):
            theta = 2 * math.pi * i / self.segments
            for j in range(self.segments):
                phi = 2 * math.pi * j / self.segments
                x = (self.R + self.r * math.cos(phi)) * math.cos(theta)
                y = (self.R + self.r * math.cos(phi)) * math.sin(theta)
                z = self.r * math.sin(phi)
                self.vertices.append((x, y, z))

    def generate_edges(self):
        for i in range(self.segments):
            for j in range(self.segments):
                current = i * self.segments + j
                next_i = (i + 1) % self.segments
                next_j = (j + 1) % self.segments
                self.edges.append((current, i * self.segments + next_j))
                self.edges.append((current, next_i * self.segments + j))

