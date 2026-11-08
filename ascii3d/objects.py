"""3D Object definitions"""

import math
from typing import List, Tuple


class Object3D:
    """Base class for 3D objects"""

    def __init__(self, name: str):
        self.name = name
        self.vertices: List[Tuple[float, float, float]] = []
        self.faces: List[List[int]] = []
        self.generated = False

    def generate(self, detail: int = 20):
        """Generate mesh - override in subclasses"""
        pass

    def get_vertices(self) -> List[Tuple[float, float, float]]:
        if not self.generated:
            self.generate()
            self.generated = True
        return self.vertices

    def get_faces(self) -> List[List[int]]:
        if not self.generated:
            self.generate()
            self.generated = True
        return self.faces


class Donut(Object3D):
    """Classic torus (donut)"""

    def __init__(self, R: float = 2.0, r: float = 0.8):
        super().__init__("donut")
        self.R = R
        self.r = r

    def generate(self, detail: int = 32):
        self.vertices = []
        self.faces = []

        for i in range(detail):
            u = 2 * math.pi * i / detail
            for j in range(detail):
                v = 2 * math.pi * j / detail

                x = (self.R + self.r * math.cos(v)) * math.cos(u)
                y = (self.R + self.r * math.cos(v)) * math.sin(u)
                z = self.r * math.sin(v)

                self.vertices.append((x, y, z))

        for i in range(detail):
            for j in range(detail):
                i_next = (i + 1) % detail
                j_next = (j + 1) % detail
                a = i * detail + j
                b = i * detail + j_next
                c = i_next * detail + j_next
                d = i_next * detail + j
                self.faces.append([a, b, c, d])


class Cube(Object3D):
    """Simple cube"""

    def __init__(self, size: float = 1.5):
        super().__init__("cube")
        self.size = size

    def generate(self, detail: int = 10):
        s = self.size
        self.vertices = [
            (-s, -s, -s), (s, -s, -s), (s, s, -s), (-s, s, -s),
            (-s, -s, s), (s, -s, s), (s, s, s), (-s, s, s)
        ]
        self.faces = [
            [0, 1, 2, 3],
            [4, 7, 6, 5],
            [0, 4, 5, 1],
            [2, 6, 7, 3],
            [1, 5, 6, 2],
            [4, 0, 3, 7],
        ]


class Sphere(Object3D):
    """Sphere using latitude/longitude"""

    def __init__(self, radius: float = 1.5):
        super().__init__("sphere")
        self.radius = radius

    def generate(self, detail: int = 24):
        self.vertices = []
        self.faces = []

        for i in range(detail + 1):
            lat = math.pi * i / detail
            for j in range(detail):
                lon = 2 * math.pi * j / detail

                x = self.radius * math.sin(lat) * math.cos(lon)
                y = self.radius * math.sin(lat) * math.sin(lon)
                z = self.radius * math.cos(lat)

                self.vertices.append((x, y, z))

        for i in range(detail):
            for j in range(detail):
                j_next = (j + 1) % detail
                a = i * detail + j
                b = i * detail + j_next
                c = (i + 1) * detail + j_next
                d = (i + 1) * detail + j
                self.faces.append([a, b, c, d])


class Knot(Object3D):
    """Torus knot"""

    def __init__(self, p: int = 3, q: int = 2):
        super().__init__("knot")
        self.p = p
        self.q = q

    def generate(self, detail: int = 64):
        self.vertices = []
        self.faces = []

        for i in range(detail):
            u = 2 * math.pi * i / detail
            for j in range(12):
                v = 2 * math.pi * j / 12

                R = 2.0
                r = 0.6

                x = (R + r * math.cos(self.q * v)) * math.cos(self.p * u)
                y = (R + r * math.cos(self.q * v)) * math.sin(self.p * u)
                z = r * math.sin(self.q * v)

                self.vertices.append((x, y, z))

        for i in range(detail):
            for j in range(11):
                i_next = (i + 1) % detail
                a = i * 12 + j
                b = i * 12 + j + 1
                c = i_next * 12 + j + 1
                d = i_next * 12 + j
                self.faces.append([a, b, c, d])


class Plasma(Object3D):
    """Plasma effect - procedural"""

    def __init__(self):
        super().__init__("plasma")
        self.time = 0

    def generate(self, detail: int = 32):
        self.vertices = []
        self.faces = []

        for i in range(detail + 1):
            x = (i / detail - 0.5) * 4
            for j in range(detail + 1):
                z = (j / detail - 0.5) * 4

                # Plasma-like height
                y = math.sin(x * 3 + self.time) * math.cos(z * 3 + self.time) * 0.5
                y += math.sin(x * 6 - self.time * 1.5) * 0.3

                self.vertices.append((x, y, z))

        for i in range(detail):
            for j in range(detail):
                a = i * (detail + 1) + j
                b = i * (detail + 1) + j + 1
                c = (i + 1) * (detail + 1) + j + 1
                d = (i + 1) * (detail + 1) + j
                self.faces.append([a, b, c, d])

    def update(self, dt: float):
        self.time += dt


class Fire(Object3D):
    """Fire effect - billboarding planes"""

    def __init__(self):
        super().__init__("fire")

    def generate(self, detail: int = 20):
        self.vertices = []
        self.faces = []

        # Simple flame shape
        for i in range(detail):
            y = i / detail * 3
            radius = 1.0 * (1 - y / 3) ** 0.5
            for j in range(16):
                angle = 2 * math.pi * j / 16
                x = radius * math.cos(angle) * (0.8 + 0.2 * math.sin(y * 5))
                z = radius * math.sin(angle) * (0.8 + 0.2 * math.cos(y * 5))

                self.vertices.append((x, y, z))

        for i in range(detail - 1):
            for j in range(16):
                j_next = (j + 1) % 16
                a = i * 16 + j
                b = i * 16 + j_next
                c = (i + 1) * 16 + j_next
                d = (i + 1) * 16 + j
                self.faces.append([a, b, c, d])


class Flow(Object3D):
    """Flow field - wavy surface"""

    def __init__(self):
        super().__init__("flow")

    def generate(self, detail: int = 32):
        self.vertices = []
        self.faces = []

        for i in range(detail + 1):
            x = (i / detail - 0.5) * 6
            for j in range(detail + 1):
                z = (j / detail - 0.5) * 6

                # Flow pattern
                y = math.sin(x * 2) * math.cos(z * 2) * 0.5
                y += math.sin((x + z) * 3) * 0.3

                self.vertices.append((x, y, z))

        for i in range(detail):
            for j in range(detail):
                a = i * (detail + 1) + j
                b = i * (detail + 1) + j + 1
                c = (i + 1) * (detail + 1) + j + 1
                d = (i + 1) * (detail + 1) + j
                self.faces.append([a, b, c, d])


class Stars(Object3D):
    """Star field - point cloud"""

    def __init__(self):
        super().__init__("stars")

    def generate(self, detail: int = 500):
        self.vertices = []
        self.faces = []

        # Random star points
        import random
        random.seed(42)
        for _ in range(detail):
            x = random.uniform(-5, 5)
            y = random.uniform(-5, 5)
            z = random.uniform(-5, 5)
            self.vertices.append((x, y, z))

        # No faces, just points


def create_object(name: str) -> Object3D:
    """Factory function to create objects"""
    objects = {
        'donut': Donut,
        'cube': Cube,
        'sphere': Sphere,
        'knot': Knot,
        'plasma': Plasma,
        'fire': Fire,
        'flow': Flow,
        'stars': Stars,
    }

    obj_class = objects.get(name.lower())
    if obj_class:
        return obj_class()
    return Donut()


def list_objects():
    """List available objects"""
    return ['donut', 'cube', 'sphere', 'knot', 'plasma', 'fire', 'flow', 'stars']
