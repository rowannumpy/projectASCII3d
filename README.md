# ASCII3D - Terminal ASCII 3D Animation Engine

A terminal-based ASCII 3D animation engine replicating the features of [ascii.krackeddevs.com](https://ascii.krackeddevs.com/).

## Features

- **8 Objects**: donut, cube, sphere, knot, plasma, fire, flow, stars
- **11 Charsets**: standard, blocks, dots, binary, donut, photo, bars, shade, braille, stars, circles
- **11 Looks**: neo, solaris, blueprint, mono, signal, ember, inferno, drift, aurora, voltage, noir (with ANSI colors)
- **Motion Controls**: speed, cell, contrast
- **Artboard**: Custom size settings
- **Real-time animation** in terminal

## Installation

```bash
# Clone or copy to your project
cd ascii3d
python -m pip install -e .
```

## Usage

### CLI Commands

```bash
# Launch animation
python -m ascii3d generate donut

# Set charset
python -m ascii3d charset standard

# Set motion parameters
python -m ascii3d motion speed 85
python -m ascii3d motion cell 18
python -m ascii3d motion contrast 100

# Set look style
python -m ascii3d looks neo

# Set artboard size
python -m ascii3d size 1080 1080

# Set FPS
python -m ascii3d fps 60

# List options
python -m ascii3d list objects
python -m ascii3d list charsets
python -m ascii3d list looks

# Help
python -m ascii3d help
```

### Interactive Controls

During animation, use these keys:

| Key | Action |
|-----|--------|
| `q` / `Q` | Quit |
| `Space` | Pause/Resume |
| `+` / `-` | Speed up/down |
| `1-8` | Switch objects |
| `c` | Cycle charset |
| `l` | Cycle look |
| `r` | Reset rotation |
| `h` | Show help |

## Objects

1. **donut** - Classic rotating torus
2. **cube** - Rotating cube
3. **sphere** - Rotating sphere
4. **knot** - Torus knot
5. **plasma** - Plasma effect
6. **fire** - Fire effect
7. **flow** - Flow field
8. **stars** - Star field

## Charsets

- standard - Standard ASCII density
- blocks - Block characters
- dots - Dot matrix
- binary - Binary 01
- donut - Donut optimized
- photo - Photographic rendering
- bars - Bar graph style
- shade - Shading characters
- braille - Braille patterns
- stars - Star characters
- circles - Circle characters

## Looks

- neo - Neo style (green/cyan)
- solaris - Solaris style (orange)
- blueprint - Blueprint style (cyan/white)
- mono - Monochrome
- signal - Signal style (green matrix)
- ember - Ember style (red/orange)
- inferno - Inferno style (red)
- drift - Drift style (blue)
- aurora - Aurora style (magenta)
- voltage - Voltage style (purple)
- noir - Noir style (gray)

## Motion Parameters

- **speed** (0-100) - Animation speed
- **cell** (0-100) - Character cell size/detail
- **contrast** (0-100) - Contrast level

## Artboard Sizes

Supports various aspect ratios:
- Square 1:1
- Landscape 3:2
- Portrait 4:5
- Widescreen 16:9
- Banner 3:1
- Custom (specify width height)

## Requirements

- Python 3.8+
- Windows or Unix terminal with ANSI support
- 80x24 minimum terminal size

## License

MIT

## Original

Based on ascii.krackeddevs.com design
# projectASCII3d