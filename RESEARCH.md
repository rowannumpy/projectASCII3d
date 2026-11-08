# ASCII Art Generator Research - ascii.krackeddevs.com

## Website Analysis

Based on screenshots and web fetch research, this is a browser-based ASCII art generator that creates 3D ASCII animations using WebGL/WebGPU with ASCII character rendering.

## Key Findings

### Engine Objects (12 total)
From web fetch and screenshots:
1. **donut** - Classic rotating donut (torus)
2. **cube** - Rotating cube
3. **sphere** - Rotating sphere
4. **knot** - Torus knot
5. **pyramid** - Crossed out in screenshot (may be disabled)
6. **matrix** - Crossed out in screenshot (may be disabled)
7. **plasma** - Plasma effect
8. **life** - Crossed out in screenshot (may be disabled)
9. **fire** - Fire effect
10. **flow** - Flow field
11. **stars** - Star field
12. **tunnel** - Crossed out in screenshot (may be disabled)

**Active objects visible**: donut, cube, sphere, knot, plasma, fire, flow, stars (8 objects)

### Charsets (11 total)
1. **standard** - Standard ASCII density characters
2. **blocks** - Block characters
3. **dots** - Dot matrix pattern
4. **binary** - 01 binary
5. **donut** - Donut-specific charset
6. **photo** - Photographic rendering
7. **bars** - Bar graph style
8. **shade** - Shading characters
9. **braille** - Braille patterns
10. **stars** - Star characters
11. **circles** - Circle characters

### Looks (11 total)
1. **neo** - Neo style
2. **solaris** - Solaris style
3. **blueprint** - Blueprint style
4. **mono** - Monochrome
5. **signal** - Signal style
6. **ember** - Ember style
7. **inferno** - Inferno style
8. **drift** - Drift style
9. **aurora** - Aurora style
10. **voltage** - Voltage style
11. **noir** - Noir style

### Motion Controls
From screenshots:
- **SPEED** (slider 0-100, shown at 85)
- **CELL** (slider 0-100, shown at 18)
- **CONTRAST** (slider 0-100, shown at 100)
- **pause** (button)

### Artboard Controls
- Aspect ratios:
  - Square 1:1
  - Landscape 3:2
  - Portrait 4:5
  - Widescreen 16:9
  - Banner 3:1
  - Custom size
- Default size shown: 1080x1080 (from screenshot)
- Web fetch shows default: 1200x800

## Command Structure Requested

User wants hierarchical command structure:
```
ascii3d
generate / charset / motion / looks / size / help / list charsets / list looks / list objects / fps
generate > donut / cube / sphere etc
charset > standard / blocks / docs ect
motion > speed / cell / contrast
looks > neo / solaris / blueprint ect
size > <width> <height>
help > lists commands
```

## Clarification Questions

Based on this research, I need clarification on:

1. **Platform**: The website is a web app. User asked for "terminal fish" initially. Do they want:
   - Terminal CLI that mimics the web UI?
   - Terminal with interactive TUI?
   - Or just replicate the rendering engine in terminal?

2. **Disabled objects**: Pyramid, matrix, life, tunnel are crossed out in screenshot. Are these truly unavailable or just not selected?

3. **Looks vs Charsets**: Looks seem to be visual styles (possibly color palettes or character mappings). Are these separate from charsets or are looks combinations of charsets?

4. **CELL parameter**: What does CELL control? Character size? Resolution? Cell count for rendering?

5. **No colors**: User said "no colours" but looks appear to have color schemes (neo, ember, etc). Should looks be grayscale ASCII only?

6. **Command structure**: The requested command structure looks like interactive commands rather than CLI args. Should I build:
   - Interactive shell with commands (like ascii3d > generate > donut)
   - Or traditional CLI with arguments (ascii3d --generate donut)?

7. **Real-time rendering**: Terminal rendering at 1080x1080 is impossible. What terminal size/resolution constraints exist?

8. **Animation quality**: Web version likely uses WebGL. Terminal ASCII at high resolution will be slow. What FPS target?

Please clarify these points before proceeding.
