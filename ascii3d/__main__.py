#!/usr/bin/env python3
"""
ascii3d - Terminal ASCII 3D Animation Engine
Replicates features of ascii.krackeddevs.com

Usage:
    ascii3d generate donut
    ascii3d charset standard
    ascii3d motion speed 85
    ascii3d looks neo
    ascii3d size 1080 1080
    ascii3d fps 60
    ascii3d help
    ascii3d list objects
    ascii3d list charsets
    ascii3d list looks
"""

import sys
import argparse
from ascii3d.engine import ASCIIEngine
from ascii3d.console import ConsoleUI


def main():
    parser = argparse.ArgumentParser(
        prog='ascii3d',
        description='Terminal ASCII 3D Animation Engine'
    )
    parser.add_argument('command', help='Command to execute')
    parser.add_argument('args', nargs='*', help='Command arguments')

    args = parser.parse_args()

    # Handle commands
    command = args.command.lower()
    cmd_args = args.args

    if command == 'help':
        print_help()
    elif command == 'list':
        if cmd_args and cmd_args[0] == 'objects':
            list_objects()
        elif cmd_args and cmd_args[0] == 'charsets':
            list_charsets()
        elif cmd_args and cmd_args[0] == 'looks':
            list_looks()
        else:
            print("Usage: ascii3d list {objects|charsets|looks}")
    elif command == 'generate':
        # Launch interactive engine with object
        object_name = cmd_args[0] if cmd_args else 'donut'
        run_engine(object_name)
    elif command == 'charset':
        # Would normally save preference
        print(f"Charset set to: {cmd_args[0] if cmd_args else 'standard'}")
    elif command == 'motion':
        # Motion controls
        if len(cmd_args) >= 2:
            param = cmd_args[0]
            value = cmd_args[1]
            print(f"Motion {param} set to: {value}")
    elif command == 'looks':
        print(f"Look set to: {cmd_args[0] if cmd_args else 'neo'}")
    elif command == 'size':
        if len(cmd_args) >= 2:
            width, height = cmd_args[0], cmd_args[1]
            print(f"Size set to: {width}x{height}")
    elif command == 'fps':
        print(f"FPS set to: {cmd_args[0] if cmd_args else '60'}")
    else:
        print(f"Unknown command: {command}")
        print_help()


def print_help():
    help_text = """
ascii3d - Terminal ASCII 3D Animation Engine

Usage:
    ascii3d generate <object>     Launch animation with object
    ascii3d charset <charset>     Set character set
    ascii3d motion <param> <val>  Set motion parameter (speed/cell/contrast)
    ascii3d looks <look>          Set visual look
    ascii3d size <w> <h>         Set artboard size
    ascii3d fps <number>         Set frames per second
    ascii3d help                 Show this help
    ascii3d list objects         List available objects
    ascii3d list charsets        List available charsets
    ascii3d list looks           List available looks

Objects:
    donut   - Classic rotating donut (torus)
    cube    - Rotating cube
    sphere  - Rotating sphere
    knot    - Torus knot
    plasma  - Plasma effect
    fire    - Fire effect
    flow    - Flow field
    stars   - Star field

Charsets:
    standard, blocks, dots, binary, donut, photo, bars, shade, braille, stars, circles

Looks:
    neo, solaris, blueprint, mono, signal, ember, inferno, drift, aurora, voltage, noir

Motion Parameters:
    speed    - Animation speed (0-100)
    cell     - Character cell size/detail (0-100)
    contrast - Contrast level (0-100)

Interactive Controls (during animation):
    q/Q      - Quit
    Space    - Pause/Resume
    +/-      - Speed up/down
    1-8      - Switch object
    c        - Cycle charset
    l        - Cycle look
    h        - Show help
    r        - Reset view
"""
    print(help_text)


def list_objects():
    objects = [
        "donut   - Classic rotating donut (torus)",
        "cube    - Rotating cube",
        "sphere  - Rotating sphere",
        "knot    - Torus knot",
        "plasma  - Plasma effect",
        "fire    - Fire effect",
        "flow    - Flow field",
        "stars   - Star field",
    ]
    print("Available Objects:")
    for obj in objects:
        print(f"  {obj}")


def list_charsets():
    charsets = [
        "standard - Standard ASCII density",
        "blocks   - Block characters",
        "dots     - Dot matrix",
        "binary   - Binary 01",
        "donut    - Donut optimized",
        "photo    - Photographic",
        "bars     - Bar graph style",
        "shade    - Shading characters",
        "braille  - Braille patterns",
        "stars    - Star characters",
        "circles  - Circle characters",
    ]
    print("Available Charsets:")
    for cs in charsets:
        print(f"  {cs}")


def list_looks():
    looks = [
        "neo      - Neo style",
        "solaris  - Solaris style",
        "blueprint- Blueprint style",
        "mono     - Monochrome",
        "signal   - Signal style",
        "ember    - Ember style",
        "inferno  - Inferno style",
        "drift    - Drift style",
        "aurora   - Aurora style",
        "voltage  - Voltage style",
        "noir     - Noir style",
    ]
    print("Available Looks:")
    for look in looks:
        print(f"  {look}")


def run_engine(object_name):
    """Launch the animation engine"""
    try:
        engine = ASCIIEngine()
        engine.set_object(object_name)
        engine.run()
    except KeyboardInterrupt:
        print("\nExiting...")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
