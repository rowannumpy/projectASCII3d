"""ASCII 3D Renderer with matrix math"""

import math
from typing import List, Tuple


class Matrix4x4:
    """4x4 transformation matrix"""

    def __init__(self):
        self.m = [[1.0 if i == j else 0.0 for j in range(4)] for i in range(4)]

    @staticmethod
    def identity():
        return Matrix4x4()

    @staticmethod
    def rotation_x(angle: float) -> 'Matrix4x4':
        m = Matrix4x4()
        c, s = math.cos(angle), math.sin(angle)
        m.m[1][1] = c
        m.m[1][2] = -s
        m.m[2][1] = s
        m.m[2][2] = c
        return m

    @staticmethod
    def rotation_y(angle: float) -> 'Matrix4x4':
        m = Matrix4x4()
        c, s = math.cos(angle), math.sin(angle)
        m.m[0][0] = c
        m.m[0][2] = s
        m.m[2][0] = -s
        m.m[2][2] = c
        return m

    @staticmethod
    def rotation_z(angle: float) -> 'Matrix4x4':
        m = Matrix4x4()
        c, s = math.cos(angle), math.sin(angle)
        m.m[0][0] = c
        m.m[0][1] = -s
        m.m[1][0] = s
        m.m[1][1] = c
        return m

    @staticmethod
    def translation(x: float, y: float, z: float) -> 'Matrix4x4':
        m = Matrix4x4()
        m.m[0][3] = x
        m.m[1][3] = y
        m.m[2][3] = z
        return m

    @staticmethod
    def perspective(fov: float, aspect: float, near: float, far: float) -> 'Matrix4x4':
        m = Matrix4x4()
        f = 1.0 / math.tan(fov / 2.0)
        m.m[0][0] = f / aspect
        m.m[1][1] = f
        m.m[2][2] = (far + near) / (near - far)
        m.m[2][3] = (2 * far * near) / (near - far)
        m.m[3][2] = -1.0
        m.m[3][3] = 0.0
        return m

    def multiply(self, other: 'Matrix4x4') -> 'Matrix4x4':
        result = Matrix4x4()
        for i in range(4):
            for j in range(4):
                result.m[i][j] = sum(self.m[i][k] * other.m[k][j] for k in range(4))
        return result

    def transform_point(self, x: float, y: float, z: float) -> Tuple[float, float, float, float]:
        w = self.m[3][0] * x + self.m[3][1] * y + self.m[3][2] * z + self.m[3][3]
        x_out = self.m[0][0] * x + self.m[0][1] * y + self.m[0][2] * z + self.m[0][3]
        y_out = self.m[1][0] * x + self.m[1][1] * y + self.m[1][2] * z + self.m[1][3]
        z_out = self.m[2][0] * x + self.m[2][1] * y + self.m[2][2] * z + self.m[2][3]
        return (x_out, y_out, z_out, w)


class FrameBuffer:
    """Frame buffer with depth testing"""

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.clear()

    def clear(self):
        self.buffer = [[' ' for _ in range(self.width)] for _ in range(self.height)]
        self.depth = [[float('inf') for _ in range(self.width)] for _ in range(self.height)]

    def set_pixel(self, x: int, y: int, z: float, char: str):
        if 0 <= x < self.width and 0 <= y < self.height:
            if z < self.depth[y][x]:
                self.depth[y][x] = z
                self.buffer[y][x] = char

    def get_frame(self) -> str:
        return '\n'.join(''.join(row) for row in self.buffer)

    def resize(self, width: int, height: int):
        self.width = width
        self.height = height
        self.clear()


class ASRenderer:
    """Core ASCII renderer"""

    def __init__(self, width: int = 80, height: int = 40):
        self.width = width
        self.height = height
        self.frame_buffer = FrameBuffer(width, height)
        self.objects = {}

    def resize(self, width: int, height: int):
        self.width = width
        self.height = height
        self.frame_buffer.resize(width, height)

    def project_point(self, x: float, y: float, z: float, w: float) -> Tuple[int, int, float]:
        """Project 3D point to 2D"""
        if abs(w) < 1e-6:
            return (-1, -1, float('inf'))

        x_ndc = x / w
        y_ndc = y / w
        z_ndc = z / w

        screen_x = int((x_ndc + 1) * 0.5 * self.width)
        screen_y = int((1 - y_ndc) * 0.5 * self.height)

        return (screen_x, screen_y, z_ndc)

    def draw_triangle(self, p1, p2, p3, char: str):
        """Draw filled triangle with depth buffer"""
        x1, y1, z1 = p1
        x2, y2, z2 = p2
        x3, y3, z3 = p3

        min_x = max(0, min(x1, x2, x3))
        max_x = min(self.width - 1, max(x1, x2, x3))
        min_y = max(0, min(y1, y2, y3))
        max_y = min(self.height - 1, max(y1, y2, y3))

        def edge(x, y, xa, ya, xb, yb):
            return (x - xa) * (yb - ya) - (y - ya) * (xb - xa)

        area = edge(x3, y3, x1, y1, x2, y2)
        if abs(area) < 1e-6:
            return

        for y in range(min_y, max_y + 1):
            for x in range(min_x, max_x + 1):
                w1 = edge(x, y, x2, y2, x3, y3) / area
                w2 = edge(x, y, x3, y3, x1, y1) / area
                w3 = edge(x, y, x1, y1, x2, y2) / area

                if w1 >= 0 and w2 >= 0 and w3 >= 0:
                    z = w1 * z1 + w2 * z2 + w3 * z3
                    self.frame_buffer.set_pixel(x, y, z, char)

    def render_object(self, obj, rot_x: float, rot_y: float, rot_z: float,
                     charset: str, look: dict, distance: float = 5.0, fov: float = 1.0):
        """Render 3D object"""
        self.frame_buffer.clear()

        # Build transform
        model = Matrix4x4.rotation_x(rot_x)
        model = model.multiply(Matrix4x4.rotation_y(rot_y))
        model = model.multiply(Matrix4x4.rotation_z(rot_z))
        model = model.multiply(Matrix4x4.translation(0, 0, -distance))

        aspect = self.width / self.height
        proj = Matrix4x4.perspective(fov, aspect, 0.1, 100.0)
        mvp = proj.multiply(model)

        vertices = obj.get_vertices()
        faces = obj.get_faces()

        if not vertices or not faces:
            return

        # Transform vertices
        transformed = []
        for v in vertices:
            x, y, z, w = mvp.transform_point(v[0], v[1], v[2])
            transformed.append((x, y, z, w))

        # Render faces
        for face in faces:
            if len(face) < 3:
                continue

            pts = [transformed[i % len(transformed)] for i in face[:3]]
            p1 = self.project_point(*pts[0])
            p2 = self.project_point(*pts[1])
            p3 = self.project_point(*pts[2])

            # Backface culling
            v1 = vertices[face[0]]
            v2 = vertices[face[1]]
            v3 = vertices[face[2]]

            ux, uy, uz = v2[0] - v1[0], v2[1] - v1[1], v2[2] - v1[2]
            vx, vy, vz = v3[0] - v1[0], v3[1] - v1[1], v3[2] - v1[2]
            nx = uy * vz - uz * vy
            nz = ux * vy - uy * vx

            if nz < 0:  # Backface
                continue

            # Lighting intensity
            intensity = max(0.2, min(1.0, 0.5 + 0.5 * math.cos(rot_y + rot_x)))

            # Map intensity to charset
            charset_str = charset['chars']
            idx = int(intensity * (len(charset_str) - 1))
            char = charset_str[idx]

            # Apply look color
            if look:
                char = f"{look['fg']}{char}{look['reset']}"

            self.draw_triangle(p1, p2, p3, char)
