"""Main ASCII 3D Engine"""

import sys
import time
import math
from ascii3d.objects import create_object, list_objects
from ascii3d.charsets import get_charset
from ascii3d.looks import get_look
from ascii3d.renderer import ASRenderer


class ASCIIEngine:
    """Main animation engine"""

    def __init__(self, width: int = 80, height: int = 40):
        self.width = width
        self.height = height
        self.renderer = ASRenderer(width, height)

        # State
        self.object_name = 'donut'
        self.obj = create_object(self.object_name)

        self.charset_name = 'standard'
        self.charset = get_charset(self.charset_name)

        self.look_name = 'mono'
        self.look = get_look(self.look_name)

        self.speed = 85  # 0-100
        self.cell = 18   # 0-100
        self.contrast = 100  # 0-100

        # Rotation
        self.rot_x = 0.0
        self.rot_y = 0.0
        self.rot_z = 0.0
        self.rot_x_speed = 0.02
        self.rot_y_speed = 0.03
        self.rot_z_speed = 0.01

        self.paused = False
        self.running = True

        # Camera
        self.distance = 5.0
        self.fov = 1.0

        # Terminal
        self._setup_terminal()

    def _setup_terminal(self):
        """Setup terminal for rendering"""
        if sys.platform == 'win32':
            import ctypes
            # Hide cursor
            kernel32 = ctypes.windll.kernel32
            handle = kernel32.GetStdHandle(-11)
            class CursorInfo(ctypes.Structure):
                _fields_ = [("dwSize", ctypes.c_int), ("bVisible", ctypes.c_bool)]
            cursor_info = CursorInfo()
            cursor_info.dwSize = 1
            cursor_info.bVisible = False
            kernel32.SetConsoleCursorInfo(handle, ctypes.byref(cursor_info))
        else:
            print('\033[?25l', end='', flush=True)

    def _restore_terminal(self):
        """Restore terminal"""
        if sys.platform == 'win32':
            import ctypes
            kernel32 = ctypes.windll.kernel32
            handle = kernel32.GetStdHandle(-11)
            class CursorInfo(ctypes.Structure):
                _fields_ = [("dwSize", ctypes.c_int), ("bVisible", ctypes.c_bool)]
            cursor_info = CursorInfo()
            cursor_info.dwSize = 1
            cursor_info.bVisible = True
            kernel32.SetConsoleCursorInfo(handle, ctypes.byref(cursor_info))
        else:
            print('\033[?25h', end='', flush=True)

    def set_object(self, name: str):
        """Change object"""
        if name in list_objects():
            self.object_name = name
            self.obj = create_object(name)
            return True
        return False

    def set_charset(self, name: str):
        """Change charset"""
        self.charset_name = name
        self.charset = get_charset(name)

    def set_look(self, name: str):
        """Change look"""
        self.look_name = name
        self.look = get_look(name)

    def resize(self, width: int, height: int):
        """Resize canvas"""
        self.width = width
        self.height = height
        self.renderer.resize(width, height)

    def _clear_screen(self):
        """Clear screen"""
        if sys.platform == 'win32':
            import ctypes
            kernel32 = ctypes.windll.kernel32
            handle = kernel32.GetStdHandle(-11)
            class Coord(ctypes.Structure):
                _fields_ = [("X", ctypes.c_short), ("Y", ctypes.c_short)]
            kernel32.SetConsoleCursorPosition(handle, Coord(0, 0))
        else:
            print('\033[H', end='', flush=True)

    def _input_poll(self):
        """Check for keyboard input (non-blocking)"""
        try:
            if sys.platform == 'win32':
                import msvcrt
                if msvcrt.kbhit():
                    ch = msvcrt.getch()
                    if isinstance(ch, bytes):
                        ch = ch.decode('utf-8', errors='ignore')
                    return ch
                return None
            else:
                import select
                if select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
                    return None
                return sys.stdin.read(1)
        except:
            return None

    def _handle_input(self):
        """Handle keyboard input"""
        ch = self._input_poll()

        if not ch:
            return

        if ch in ('q', 'Q', '\x03'):
            self.running = False
        elif ch == ' ':
            self.paused = not self.paused
        elif ch == '+':
            self.speed = min(100, self.speed + 5)
        elif ch == '-':
            self.speed = max(0, self.speed - 5)
        elif ch == '1':
            self.set_object('donut')
        elif ch == '2':
            self.set_object('cube')
        elif ch == '3':
            self.set_object('sphere')
        elif ch == '4':
            self.set_object('knot')
        elif ch == '5':
            self.set_object('plasma')
        elif ch == '6':
            self.set_object('fire')
        elif ch == '7':
            self.set_object('flow')
        elif ch == '8':
            self.set_object('stars')
        elif ch == 'c':
            # Cycle charset
            charsets = ['standard', 'blocks', 'dots', 'binary', 'donut', 'photo', 'bars', 'shade', 'braille', 'stars', 'circles']
            idx = charsets.index(self.charset_name) if self.charset_name in charsets else 0
            self.set_charset(charsets[(idx + 1) % len(charsets)])
        elif ch == 'l':
            # Cycle look
            looks = ['neo', 'solaris', 'blueprint', 'mono', 'signal', 'ember', 'inferno', 'drift', 'aurora', 'voltage', 'noir']
            idx = looks.index(self.look_name) if self.look_name in looks else 0
            self.set_look(looks[(idx + 1) % len(looks)])
        elif ch == 'r':
            # Reset rotation
            self.rot_x = self.rot_y = self.rot_z = 0.0
        elif ch == 'h':
            # Toggle help - handled in render
            pass

    def run(self):
        """Main animation loop"""
        last_time = time.time()
        frame_count = 0
        fps_start = time.time()

        try:
            while self.running:
                # Handle input
                self._handle_input()

                # Update animation
                if not self.paused:
                    dt = time.time() - last_time
                    speed_mult = self.speed / 85.0

                    self.rot_x += self.rot_x_speed * speed_mult * 60 * dt
                    self.rot_y += self.rot_y_speed * speed_mult * 60 * dt
                    self.rot_z += self.rot_z_speed * speed_mult * 60 * dt

                    # Update procedural objects
                    if hasattr(self.obj, 'update'):
                        self.obj.update(dt)

                # Render
                self.renderer.render_object(
                    self.obj, self.rot_x, self.rot_y, self.rot_z,
                    self.charset, self.look, self.distance, self.fov
                )

                # Display
                self._clear_screen()
                frame = self.renderer.get_frame()

                # Apply look colors
                if self.look:
                    print(f"{self.look['fg']}{frame}{self.look['reset']}")
                else:
                    print(frame)

                # Status line
                status = f"Object: {self.object_name:6} | Charset: {self.charset_name:8} | Look: {self.look_name:10} | Speed: {self.speed:3} | Cell: {self.cell:3} | Contrast: {self.contrast:3}"
                if self.paused:
                    status += " [PAUSED]"
                print(status)
                print("Keys: q=quit  Space=pause  +/-=speed  1-8=object  c=charset  l=look  r=reset")

                frame_count += 1

                # FPS limiting
                current_time = time.time()
                elapsed = current_time - last_time
                target_frame = 1.0 / 30.0
                sleep_time = max(0, target_frame - elapsed)
                if sleep_time > 0:
                    time.sleep(sleep_time)
                last_time = current_time

        except KeyboardInterrupt:
            pass
        finally:
            self._restore_terminal()
            print("\nThanks for using ascii3d!")
