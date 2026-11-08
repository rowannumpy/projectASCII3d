# ASCII 3D Animation Engine - Build Plan

**Replicates:** https://ascii.krackeddevs.com/

## Project Overview

A terminal-based ASCII animation engine that renders 3D objects and effects with:
- Multiple 3D objects/primitives
- Multiple character sets (charsets)
- Multiple visual styles/looks
- Motion/animation effects
- Full artboard controls (camera, projection, lighting)
- Cross-platform (Windows/macOS/Linux)
- No colors - pure ASCII

---

## Command Structure

```
ascii3d [OPTIONS] [OBJECT]

Objects:
  generate    - Procedural generation showcase
  donut       - Classic rotating donut (torus)
  cube        - Rotating cube
  sphere      - Rotating sphere
  knot        - Torus knot
  plasma      - Plasma effect
  fire        - Fire effect
  flow        - Flow field / vector field
  stars       - Star field / space
  tunnel      - Infinite tunnel

Options:
  --charset CHARSET     Character set to use (default: standard)
  --look LOOK           Visual style (default: solid)
  --motion MOTION       Animation motion type (default: rotate)
  --width WIDTH         Artboard width (default: terminal width)
  --height HEIGHT       Artboard height (default: terminal height)
  --fps FPS             Target FPS (default: 60)
  --speed SPEED         Animation speed multiplier (default: 1.0)
  --distance DIST       Camera distance (default: 5.0)
  --fov FOV             Field of view in radians (default: 1.0)
  --help                Show help
  --list-charsets       List available charsets
  --list-looks          List available looks
  --list-motions        List available motions
  --list-objects        List available objects
```

### Interactive Controls (when running)

| Key | Action |
|-----|--------|
| `q` / `Q` / `Ctrl+C` | Quit |
| `Space` | Pause/Resume |
| `+` / `=` | Increase speed |
| `-` / `_` | Decrease speed |
| `w` / `s` | Rotate X faster/slower |
| `a` / `d` | Rotate Y faster/slower |
| `z` / `x` | Rotate Z faster/slower |
| `r` | Reset rotation speeds |
| `1-9` | Switch object |
| `[` / `]` | Decrease/Increase width |
| `;` / `'` | Decrease/Increase height |
| `f` | Toggle fullscreen |
| `h` | Toggle help |
| `↑` / `↓` | Zoom in/out (distance) |
| `←` / `→` | Decrease/Increase FOV |
| `c` | Cycle charset |
| `l` | Cycle look |
| `m` | Cycle motion |
| `,` / `.` | Previous/Next object |

---

## Objects (10 Total)

### 1. generate - Procedural Generation Showcase
Cycles through multiple procedural patterns:
- Perlin noise terrain
- Fractal landscapes
- Cellular automata
- Reaction-diffusion
- L-system plants
- Mandelbrot/Julia sets

### 2. donut - Classic Torus (Donut)
- Standard torus parametric: `(R + r*cos(v))*cos(u), (R + r*cos(v))*sin(u), r*sin(v)`
- R=2.0, r=0.8
- Full 3D rotation on all axes
- Configurable detail level

### 3. cube - Rotating Cube
- 8 vertices, 6 faces (quads)
- Wireframe or solid modes
- Edge highlighting option

### 4. sphere - Sphere
- Latitude/longitude tessellation
- Configurable subdivisions
- UV sphere or icosphere option

### 5. knot - Torus Knot
- Parametric: `p=3, q=2` (trefoil) by default
- Configurable p, q parameters
- Tube thickness control

### 6. plasma - Plasma Effect
- Multi-layer sine wave interference
- Palette cycling through charset
- Configurable frequency/amplitude per layer
- Time-based animation

### 7. fire - Fire Effect
- Particle-based rising flames
- Heat diffusion simulation
- Cooling at top
- Configurable intensity, spread

### 8. flow - Flow Field
- 2D vector field visualization
- Perlin noise based directions
- Particle tracing
- Streamlines or particles mode

### 9. stars - Star Field
- 3D starfield with perspective
- Parallax layers
- Twinkling effect
- Configurable density, speed

### 10. tunnel - Infinite Tunnel
- Ring segments receding into distance
- Texture mapping on rings
- Rotation + forward motion
- Configurable segment count, texture

---

## Charsets (12+ Total)

Each charset maps intensity (0.0-1.0) to characters:

| ID | Name | Characters | Description |
|----|------|------------|-------------|
| 1 | `standard` | ` .:-=+*#%@` | 10-level classic |
| 2 | `block` | ` ░▒▓█` | 5-level blocks |
| 3 | `braille` | `⠁⠂⠄⡀⢀⠈⠐⠠⡈⡐⡠⢈⢐⢠⣀⣐⣠⢀⢐⢠⣈⣐⣠⣈⣐⣠⣿` | 256 braille patterns |
| 4 | `ascii_full` | ` .'`^",:;Il!i><~+_-?][}{1)(|\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$` | 70-char full range |
| 5 | `minimal` | ` .oO@` | 5-char minimal |
| 6 | `shades` | ` ▁▂▃▄▅▆▇█` | 9-level lower blocks |
| 7 | `binary` | ` 01` | Binary only |
| 8 | `density` | ` .,;:!|+*#@` | 11-char density |
| 9 | `technical` | ` ·.•●◐◑◒◓◔◕◖◗◘◙◚◛◜◝◞◟◆◇◈◉◊○◌◍◎●` | Technical symbols |
| 10 | `geometric` | ` ▏▎▍▌▋▊▉█▉▊▋▌▍▎▏` | Vertical bars |
| 11 | `dots` | ` ⠂⠄⠆⡀⢀⠈⠐⠠⡈⡐⡠⢈⢐⢠⣀⣐⣠⣄⣆⣇⣈⣉⣊⣋⣌⣍⣎⣏⣐⣑⣒⣓⣔⣕⣖⣗⣘⣙⣚⣛⣜⣝⣞⣟⣠⣡⣢⣣⣤⣥⣦⣧⣨⣩⣪⣫⣬⣭⣮⣯⣰⣱⣲⣳⣴⣵⣶⣷⣸⣹⣺⣻⣼⣽⣾⣿` | Dot matrix |
| 12 | `custom` | User-defined via `--charset-string` | Custom string |

---

## Looks (8 Total)

Visual rendering styles for 3D objects:

| ID | Name | Description |
|----|------|-------------|
| 1 | `solid` | Filled faces with lighting/shading |
| 2 | `wireframe` | Edges only, no fill |
| 3 | `points` | Vertices only as points |
| 4 | `silhouette` | Outline only, filled interior |
| 5 | `xray` | See-through wireframe with depth fade |
| 6 | `normal` | Face normals visualized as chars |
| 7 | `depth` | Depth-based coloring (near=dense, far=sparse) |
| 8 | `contour` | Contour lines at depth intervals |

---

## Motions (10 Total)

Animation motion types:

| ID | Name | Description |
|----|------|-------------|
| 1 | `rotate` | Continuous rotation on X, Y, Z axes |
| 2 | `orbit` | Camera orbits around object |
| 3 | `tumble` | Chaotic tumbling motion |
| 4 | `wave` | Sine wave deformation |
| 5 | `pulse` | Scale pulsing (breathing) |
| 6 | `morph` | Morph between shapes |
| 7 | `drift` | Slow drift with rotation |
| 8 | `spin` | High-speed single-axis spin |
| 9 | `pendulum` | Pendulum swing motion |
| 10 | `custom` | User-defined via script |

---

## Artboard Features (Camera, Projection, Lighting)

### Camera
- **Position**: 3D position (default: 0, 0, -distance)
- **Target**: Look-at point (default: 0, 0, 0)
- **Up vector**: Camera up direction (default: 0, 1, 0)
- **Distance**: Zoom level (1.0 - 50.0)
- **Auto-rotate**: Camera orbits target

### Projection
- **Type**: Perspective / Orthographic
- **FOV**: Field of view (0.3 - π/2 radians)
- **Aspect**: Width/Height ratio (auto from terminal)
- **Near/Far planes**: 0.1 / 100.0

### Lighting
- **Type**: Directional / Point / Ambient
- **Direction**: Light vector (default: 0.5, 0.5, -1.0)
- **Intensity**: 0.0 - 2.0
- **Ambient**: Base illumination (0.0 - 1.0)
- **Specular**: Highlight intensity (0.0 - 1.0)
- **Shininess**: Specular exponent (1 - 128)

### Shading Models
- `flat` - Per-face constant shading
- `gouraud` - Interpolated vertex normals
- `phong` - Per-pixel (per-char) lighting
- `cel` - Toon/cel shading with bands
- `unlit` - No lighting, pure depth

### Post-Processing
- **Dithering**: Ordered/Bayer dithering for gradients
- **Scanlines**: Horizontal line effect
- **Vignette**: Darken edges
- **Noise**: Film grain overlay
- **Blur**: Depth-based blur (limited in ASCII)

---

## Architecture

### Core Modules

```
ascii3d/
├── __main__.py           # Entry point, CLI parsing
├── config.py             # Configuration dataclasses
├── objects/
│   ├── __init__.py
│   ├── base.py           # Object3D base class
│   ├── donut.py
│   ├── cube.py
│   ├── sphere.py
│   ├── knot.py
│   ├── generate.py
│   ├── plasma.py
│   ├── fire.py
│   ├── flow.py
│   ├── stars.py
│   └── tunnel.py
├── charsets/
│   ├── __init__.py
│   └── registry.py       # All charset definitions
├── looks/
│   ├── __init__.py
│   └── registry.py       # All look implementations
├── motions/
│   ├── __init__.py
│   └── registry.py       # All motion implementations
├── artboard/
│   ├── __init__.py
│   ├── camera.py
│   ├── projection.py
│   ├── lighting.py
│   └── shading.py
├── renderer/
│   ├── __init__.py
│   ├── matrix.py         # 4x4 matrix math
│   ├── rasterizer.py     # Triangle rasterization
│   ├── depth_buffer.py
│   └── frame_buffer.py
├── input/
│   ├── __init__.py
│   └── handler.py        # Cross-platform input
├── terminal/
│   ├── __init__.py
│   ├── capabilities.py   # Terminal detection
│   └── ansi.py           # ANSI escape codes
└── app.py                # Main application loop
```

---

## Implementation Phases

### Phase 1: Core Infrastructure (Week 1)
- [ ] Cross-platform terminal handling (Windows/Unix)
- [ ] Matrix math (4x4 transform, perspective)
- [ ] Frame buffer + depth buffer
- [ ] Triangle rasterizer with barycentric coords
- [ ] Basic CLI argument parsing
- [ ] Input handler (raw mode, escape sequences)

### Phase 2: Base Objects (Week 1-2)
- [ ] Object3D base class
- [ ] Donut (torus)
- [ ] Cube
- [ ] Sphere
- [ ] Torus Knot
- [ ] Vertex/face generation with configurable detail

### Phase 3: Charsets & Looks (Week 2)
- [ ] Charset registry with 12+ charsets
- [ ] Look registry with 8 looks
- [ ] Lighting system (directional, point, ambient)
- [ ] Shading models (flat, gouraud, phong, cel, unlit)

### Phase 4: Effects Objects (Week 2-3)
- [ ] Plasma (multi-layer sine interference)
- [ ] Fire (particle + diffusion)
- [ ] Flow field (Perlin noise vectors)
- [ ] Stars (3D starfield)
- [ ] Tunnel (ring segments)
- [ ] Generate (procedural showcase)

### Phase 5: Motions (Week 3)
- [ ] Motion registry with 10 motions
- [ ] Time-based animation system
- [ ] Motion blending/transitions

### Phase 6: Artboard (Week 3-4)
- [ ] Camera system (position, target, orbit)
- [ ] Projection (perspective/orthographic)
- [ ] Full lighting setup
- [ ] Post-processing effects

### Phase 7: Polish & CLI (Week 4)
- [ ] Interactive controls
- [ ] Help system
- [ ] Config file support
- [ ] Performance optimization
- [ ] Documentation

---

## Technical Details

### Triangle Rasterization
- Barycentric coordinate interpolation
- Depth buffering (z-buffer)
- Backface culling
- Per-pixel lighting (Phong)
- Character selection from charset by intensity

### Performance Targets
- 60 FPS at 120x40 on modern hardware
- <16ms frame time
- Efficient vertex transformation (SIMD-friendly)
- Minimal allocations in render loop

### Cross-Platform Considerations
- Windows: `msvcrt`, Win32 API for cursor/size
- Unix: `termios`, `tty`, `select`, ANSI escapes
- Terminal capability detection
- Graceful degradation

### Memory Management
- Pre-allocated buffers
- Object pooling for particles
- No GC pressure in hot path

---

## Configuration File

`~/.config/ascii3d/config.json`:
```json
{
  "default_object": "donut",
  "default_charset": "standard",
  "default_look": "solid",
  "default_motion": "rotate",
  "width": 120,
  "height": 40,
  "fps": 60,
  "speed": 1.0,
  "distance": 5.0,
  "fov": 1.0,
  "lighting": {
    "type": "directional",
    "direction": [0.5, 0.5, -1.0],
    "intensity": 1.0,
    "ambient": 0.2,
    "specular": 0.5,
    "shininess": 32
  },
  "shading": "phong",
  "post_processing": {
    "dithering": false,
    "scanlines": false,
    "vignette": false,
    "noise": false
  }
}
```

---

## Testing Checklist

- [ ] All 10 objects render correctly
- [ ] All 12 charsets display properly
- [ ] All 8 looks produce distinct output
- [ ] All 10 motions animate smoothly
- [ ] Camera controls work (zoom, orbit, FOV)
- [ ] Lighting affects shading correctly
- [ ] Cross-platform: Windows, Linux, macOS
- [ ] Terminal resize handling
- [ ] Ctrl+C graceful exit
- [ ] Config file loading/saving
- [ ] Help text displays correctly

---

## Future Extensions (Post-MVP)

- Audio reactivity (frequency bars)
- Shader-like custom expressions
- Multi-object scenes
- Export to GIF/MP4
- WebAssembly port
- Plugin system for custom objects