"""Console UI for interactive command mode"""

import sys


class ConsoleUI:
    """Interactive console interface"""

    def __init__(self):
        self.commands = {
            'generate': self.cmd_generate,
            'charset': self.cmd_charset,
            'motion': self.cmd_motion,
            'looks': self.cmd_looks,
            'size': self.cmd_size,
            'fps': self.cmd_fps,
            'help': self.cmd_help,
            'list': self.cmd_list,
            'quit': self.cmd_quit,
            'exit': self.cmd_quit,
        }

    def cmd_generate(self, args):
        """Generate animation with object"""
        if not args:
            print("Usage: generate <object>")
            print("Objects: donut, cube, sphere, knot, plasma, fire, flow, stars")
            return

        obj_name = args[0]
        print(f"Launching animation with object: {obj_name}")
        # Would launch engine here

    def cmd_charset(self, args):
        """Set charset"""
        if not args:
            print("Usage: charset <charset>")
            print("Charsets: standard, blocks, dots, binary, donut, photo, bars, shade, braille, stars, circles")
            return

        print(f"Charset set to: {args[0]}")

    def cmd_motion(self, args):
        """Set motion parameter"""
        if len(args) < 2:
            print("Usage: motion <speed|cell|contrast> <value>")
            return

        param, value = args[0], args[1]
        print(f"Motion {param} set to: {value}")

    def cmd_looks(self, args):
        """Set look style"""
        if not args:
            print("Usage: looks <look>")
            print("Looks: neo, solaris, blueprint, mono, signal, ember, inferno, drift, aurora, voltage, noir")
            return

        print(f"Look set to: {args[0]}")

    def cmd_size(self, args):
        """Set artboard size"""
        if len(args) < 2:
            print("Usage: size <width> <height>")
            return

        print(f"Size set to: {args[0]}x{args[1]}")

    def cmd_fps(self, args):
        """Set FPS"""
        if not args:
            print("Usage: fps <number>")
            return

        print(f"FPS set to: {args[0]}")

    def cmd_help(self, args):
        """Show help"""
        print("""
ascii3d - Terminal ASCII 3D Animation Engine

Commands:
  generate <object>    Launch animation with object
  charset <charset>    Set character set
  motion <param> <val> Set motion parameter (speed/cell/contrast)
  looks <look>         Set visual look
  size <w> <h>         Set artboard size
  fps <number>         Set frames per second
  list objects         List available objects
  list charsets        List available charsets
  list looks           List available looks
  help                 Show this help
  quit                 Exit

Objects: donut, cube, sphere, knot, plasma, fire, flow, stars
Charsets: standard, blocks, dots, binary, donut, photo, bars, shade, braille, stars, circles
Looks: neo, solaris, blueprint, mono, signal, ember, inferno, drift, aurora, voltage, noir
""")

    def cmd_list(self, args):
        """List items"""
        if not args:
            print("Usage: list {objects|charsets|looks}")
            return

        item = args[0]
        if item == 'objects':
            print("Objects:")
            print("  donut, cube, sphere, knot, plasma, fire, flow, stars")
        elif item == 'charsets':
            print("Charsets:")
            print("  standard, blocks, dots, binary, donut, photo, bars, shade, braille, stars, circles")
        elif item == 'looks':
            print("Looks:")
            print("  neo, solaris, blueprint, mono, signal, ember, inferno, drift, aurora, voltage, noir")
        else:
            print(f"Unknown item: {item}")

    def cmd_quit(self, args):
        """Exit"""
        print("Goodbye!")
        sys.exit(0)

    def run(self):
        """Run interactive console"""
        print("ascii3d - Terminal ASCII 3D Animation Engine")
        print("Type 'help' for commands, 'quit' to exit")
        print()

        while True:
            try:
                line = input("ascii3d> ").strip()
                if not line:
                    continue

                parts = line.split()
                cmd = parts[0].lower()
                args = parts[1:]

                if cmd in self.commands:
                    self.commands[cmd](args)
                else:
                    print(f"Unknown command: {cmd}")
                    print("Type 'help' for available commands")

            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except EOFError:
                print("\nGoodbye!")
                break
