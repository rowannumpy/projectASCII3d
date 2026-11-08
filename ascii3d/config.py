"""Configuration dataclasses for ASCII 3D Animation Engine"""

from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
import json
import os


@dataclass
class LightingConfig:
    """Lighting configuration"""
    light_type: str = "directional"  # directional, point, ambient
    direction: List[float] = field(default_factory=lambda: [0.5, 0.5, -1.0])
    position: List[float] = field(default_factory=lambda: [0.0, 0.0, 0.0])
    intensity: float = 1.0
    ambient: float = 0.2
    specular: float = 0.5
    shininess: float = 32.0
    color: List[float] = field(default_factory=lambda: [1.0, 1.0, 1.0])


@dataclass
class CameraConfig:
    """Camera configuration"""
    position: List[float] = field(default_factory=lambda: [0.0, 0.0, -5.0])
    target: List[float] = field(default_factory=lambda: [0.0, 0.0, 0.0])
    up: List[float] = field(default_factory=lambda: [0.0, 1.0, 0.0])
    distance: float = 5.0
    auto_orbit: bool = False
    orbit_speed: float = 0.01


@dataclass
class ProjectionConfig:
    """Projection configuration"""
    projection_type: str = "perspective"  # perspective, orthographic
    fov: float = 1.0  # radians
    aspect: float = 1.0
    near: float = 0.1
    far: float = 100.0
    ortho_scale: float = 1.0


@dataclass
class PostProcessingConfig:
    """Post-processing effects"""
    dithering: bool = False
    dither_type: str = "bayer"  # bayer, ordered, random
    scanlines: bool = False
    scanline_intensity: float = 0.3
    vignette: bool = False
    vignette_strength: float = 0.5
    noise: bool = False
    noise_intensity: float = 0.1


@dataclass
class AppConfig:
    """Main application configuration"""
    # Object settings
    object: str = "donut"
    object_params: Dict[str, Any] = field(default_factory=dict)

    # Visual settings
    charset: str = "standard"
    look: str = "solid"
    motion: str = "rotate"
    shading: str = "phong"  # flat, gouraud, phong, cel, unlit

    # Canvas settings
    width: int = 120
    height: int = 40
    fullscreen: bool = False

    # Animation settings
    fps: int = 60
    speed: float = 1.0
    paused: bool = False

    # Camera/Projection
    camera: CameraConfig = field(default_factory=CameraConfig)
    projection: ProjectionConfig = field(default_factory=ProjectionConfig)

    # Lighting
    lighting: LightingConfig = field(default_factory=LightingConfig)

    # Post-processing
    post_processing: PostProcessingConfig = field(default_factory=PostProcessingConfig)

    # Advanced
    show_help: bool = False
    show_fps: bool = True
    show_stats: bool = True

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "object": self.object,
            "object_params": self.object_params,
            "charset": self.charset,
            "look": self.look,
            "motion": self.motion,
            "shading": self.shading,
            "width": self.width,
            "height": self.height,
            "fullscreen": self.fullscreen,
            "fps": self.fps,
            "speed": self.speed,
            "camera": {
                "position": self.camera.position,
                "target": self.camera.target,
                "up": self.camera.up,
                "distance": self.camera.distance,
                "auto_orbit": self.camera.auto_orbit,
                "orbit_speed": self.camera.orbit_speed,
            },
            "projection": {
                "projection_type": self.projection.projection_type,
                "fov": self.projection.fov,
                "aspect": self.projection.aspect,
                "near": self.projection.near,
                "far": self.projection.far,
                "ortho_scale": self.projection.ortho_scale,
            },
            "lighting": {
                "light_type": self.lighting.light_type,
                "direction": self.lighting.direction,
                "position": self.lighting.position,
                "intensity": self.lighting.intensity,
                "ambient": self.lighting.ambient,
                "specular": self.lighting.specular,
                "shininess": self.lighting.shininess,
                "color": self.lighting.color,
            },
            "post_processing": {
                "dithering": self.post_processing.dithering,
                "dither_type": self.post_processing.dither_type,
                "scanlines": self.post_processing.scanlines,
                "scanline_intensity": self.post_processing.scanline_intensity,
                "vignette": self.post_processing.vignette,
                "vignette_strength": self.post_processing.vignette_strength,
                "noise": self.post_processing.noise,
                "noise_intensity": self.post_processing.noise_intensity,
            },
            "show_help": self.show_help,
            "show_fps": self.show_fps,
            "show_stats": self.show_stats,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AppConfig':
        """Create config from dictionary"""
        config = cls()

        # Simple fields
        for key in ["object", "object_params", "charset", "look", "motion",
                    "shading", "width", "height", "fullscreen", "fps",
                    "speed", "show_help", "show_fps", "show_stats"]:
            if key in data:
                setattr(config, key, data[key])

        # Nested objects
        if "camera" in data:
            cam = data["camera"]
            config.camera = CameraConfig(
                position=cam.get("position", [0.0, 0.0, -5.0]),
                target=cam.get("target", [0.0, 0.0, 0.0]),
                up=cam.get("up", [0.0, 1.0, 0.0]),
                distance=cam.get("distance", 5.0),
                auto_orbit=cam.get("auto_orbit", False),
                orbit_speed=cam.get("orbit_speed", 0.01),
            )

        if "projection" in data:
            proj = data["projection"]
            config.projection = ProjectionConfig(
                projection_type=proj.get("projection_type", "perspective"),
                fov=proj.get("fov", 1.0),
                aspect=proj.get("aspect", 1.0),
                near=proj.get("near", 0.1),
                far=proj.get("far", 100.0),
                ortho_scale=proj.get("ortho_scale", 1.0),
            )

        if "lighting" in data:
            light = data["lighting"]
            config.lighting = LightingConfig(
                light_type=light.get("light_type", "directional"),
                direction=light.get("direction", [0.5, 0.5, -1.0]),
                position=light.get("position", [0.0, 0.0, 0.0]),
                intensity=light.get("intensity", 1.0),
                ambient=light.get("ambient", 0.2),
                specular=light.get("specular", 0.5),
                shininess=light.get("shininess", 32.0),
                color=light.get("color", [1.0, 1.0, 1.0]),
            )

        if "post_processing" in data:
            pp = data["post_processing"]
            config.post_processing = PostProcessingConfig(
                dithering=pp.get("dithering", False),
                dither_type=pp.get("dither_type", "bayer"),
                scanlines=pp.get("scanlines", False),
                scanline_intensity=pp.get("scanline_intensity", 0.3),
                vignette=pp.get("vignette", False),
                vignette_strength=pp.get("vignette_strength", 0.5),
                noise=pp.get("noise", False),
                noise_intensity=pp.get("noise_intensity", 0.1),
            )

        return config


def load_config(config_path: Optional[str] = None) -> AppConfig:
    """Load configuration from file"""
    if config_path is None:
        # Default config locations
        config_dirs = [
            os.path.expanduser("~/.config/ascii3d"),
            os.path.expanduser("~/AppData/Roaming/ascii3d"),
            os.path.expanduser("~/.ascii3d"),
        ]

        for config_dir in config_dirs:
            config_file = os.path.join(config_dir, "config.json")
            if os.path.exists(config_file):
                config_path = config_file
                break

    if config_path and os.path.exists(config_path):
        try:
            with open(config_path, 'r') as f:
                data = json.load(f)
            return AppConfig.from_dict(data)
        except Exception:
            pass

    return AppConfig()


def save_config(config: AppConfig, config_path: Optional[str] = None) -> bool:
    """Save configuration to file"""
    if config_path is None:
        config_dir = os.path.expanduser("~/.config/ascii3d")
        os.makedirs(config_dir, exist_ok=True)
        config_path = os.path.join(config_dir, "config.json")

    try:
        with open(config_path, 'w') as f:
            json.dump(config.to_dict(), f, indent=2)
        return True
    except Exception:
        return False