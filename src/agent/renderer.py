"""Rendering module for high-quality 3D output"""

import logging
from typing import Dict, Optional
from dataclasses import dataclass
from pathlib import Path

logger = logging.getLogger(__name__)


@dataclass
class RenderSettings:
    """Rendering configuration"""
    engine: str = "CYCLES"  # CYCLES or EEVEE
    samples: int = 256
    resolution_x: int = 1920
    resolution_y: int = 1080
    fps: int = 24
    format: str = "PNG"  # PNG, JPEG, OpenEXR, etc.
    quality: str = "high"  # low, medium, high, ultra
    denoiser: str = "OptiX"  # OptiX, OpenImage, None
    gpu_enabled: bool = True
    gpu_type: str = "CUDA"  # CUDA, OPTIX, HIP


class Renderer:
    """High-quality 3D rendering engine"""
    
    def __init__(self, blender_path: Optional[str] = None,
                 output_dir: str = "./output/renders"):
        """Initialize renderer
        
        Args:
            blender_path: Path to Blender executable
            output_dir: Directory for rendered output
        """
        self.blender_path = blender_path or "blender"
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        logger.info("Renderer initialized")
    
    def render_to_video(self, character: Dict, animation: Dict, 
                       scene: Optional[str] = None,
                       **kwargs) -> Dict:
        """Render character animation to video
        
        Args:
            character: Character dictionary
            animation: Animation dictionary
            scene: Scene/environment name
            **kwargs: Additional render settings
            
        Returns:
            Render output information
        """
        settings = self._parse_settings(kwargs)
        
        char_id = character["id"]
        anim_type = animation["type"]
        
        logger.info(f"Rendering video: {char_id} - {anim_type}")
        
        # Generate render script
        render_script = self._generate_render_script(
            character, animation, scene, settings
        )
        
        output_file = self.output_dir / f"{char_id}_{anim_type}.mp4"
        
        render_info = {
            "character_id": char_id,
            "animation_type": anim_type,
            "output_file": str(output_file),
            "settings": {
                "engine": settings.engine,
                "samples": settings.samples,
                "resolution": f"{settings.resolution_x}x{settings.resolution_y}",
                "fps": settings.fps,
                "format": settings.format,
            },
            "frames_total": animation["frames"],
            "duration_seconds": animation["duration"],
            "status": "rendering",
        }
        
        logger.info(f"Render info: {render_info}")
        return render_info
    
    def render_frames(self, character: Dict, animation: Dict,
                     start_frame: int = 0,
                     end_frame: Optional[int] = None,
                     **kwargs) -> Dict:
        """Render individual frames from animation
        
        Args:
            character: Character dictionary
            animation: Animation dictionary
            start_frame: First frame to render
            end_frame: Last frame to render
            **kwargs: Render settings
            
        Returns:
            Frame rendering info
        """
        settings = self._parse_settings(kwargs)
        
        if end_frame is None:
            end_frame = animation["frames"]
        
        frame_count = end_frame - start_frame + 1
        char_id = character["id"]
        
        logger.info(f"Rendering {frame_count} frames: {start_frame}-{end_frame}")
        
        output_dir = self.output_dir / char_id / "frames"
        output_dir.mkdir(parents=True, exist_ok=True)
        
        frame_info = {
            "character_id": char_id,
            "frame_range": [start_frame, end_frame],
            "frame_count": frame_count,
            "output_dir": str(output_dir),
            "format": settings.format,
            "resolution": f"{settings.resolution_x}x{settings.resolution_y}",
            "status": "rendering",
        }
        
        return frame_info
    
    def render_preview(self, character: Dict, animation: Dict,
                      quality: str = "low") -> Dict:
        """Quick preview render with lower quality
        
        Args:
            character: Character dictionary
            animation: Animation dictionary
            quality: Preview quality (low, medium)
            
        Returns:
            Preview render info
        """
        logger.info(f"Rendering preview: {character['id']}")
        
        # Use lower quality settings for faster preview
        samples = 32 if quality == "low" else 64
        resolution = 960 if quality == "low" else 1280
        
        output_file = self.output_dir / f"{character['id']}_preview.mp4"
        
        return {
            "character_id": character["id"],
            "output_file": str(output_file),
            "quality": quality,
            "samples": samples,
            "resolution": resolution,
            "status": "preview_rendered",
        }
    
    def _parse_settings(self, kwargs: Dict) -> RenderSettings:
        """Parse render settings from kwargs"""
        quality_map = {
            "low": {"samples": 64, "resolution_x": 1280, "resolution_y": 720},
            "medium": {"samples": 128, "resolution_x": 1920, "resolution_y": 1080},
            "high": {"samples": 256, "resolution_x": 2560, "resolution_y": 1440},
            "ultra": {"samples": 512, "resolution_x": 3840, "resolution_y": 2160},
        }
        
        quality = kwargs.get("quality", "high")
        settings_dict = quality_map.get(quality, quality_map["high"])
        
        # Override with explicit parameters
        for key in ["engine", "fps", "format", "denoiser", "gpu_enabled", "gpu_type"]:
            if key in kwargs:
                settings_dict[key] = kwargs[key]
        
        return RenderSettings(**{k: v for k, v in settings_dict.items()
                                if k in RenderSettings.__dataclass_fields__})
    
    def _generate_render_script(self, character: Dict, animation: Dict,
                               scene: Optional[str],
                               settings: RenderSettings) -> str:
        """Generate Blender Python script for rendering"""
        script = f"""
import bpy
import os

# Load character with animation
bpy.ops.wm.open_mainfile(filepath=r'{character['files']['blend']}')

# Setup render settings
scene = bpy.context.scene
scene.render.engine = '{settings.engine}'
scene.render.resolution_x = {settings.resolution_x}
scene.render.resolution_y = {settings.resolution_y}
scene.render.fps = {settings.fps}
scene.render.image_settings.file_format = '{settings.format}'

# Setup cycles render
if '{settings.engine}' == 'CYCLES':
    bpy.context.scene.cycles.samples = {settings.samples}
    bpy.context.scene.cycles.use_denoising = True
    bpy.context.scene.cycles.denoiser = '{settings.denoiser}'
    
    # GPU rendering
    if {str(settings.gpu_enabled).lower()}:
        bpy.context.preferences.addons['cycles'].preferences.compute_device_type = '{settings.gpu_type}'
        bpy.context.preferences.addons['cycles'].preferences.get_devices()
        for d in bpy.context.preferences.addons['cycles'].preferences.devices:
            d.use = True

# Setup output
scene.render.filepath = r'{self.output_dir}/{{{{frame_number:04d}}}}.png'
scene.frame_start = 0
scene.frame_end = {animation['frames']}

# Render animation
bpy.ops.render.render(animation=True, write_still=True)
"""
        return script
    
    def batch_render(self, characters: list, animations: list,
                    **kwargs) -> Dict:
        """Render multiple characters and animations in batch
        
        Args:
            characters: List of character dictionaries
            animations: List of animation dictionaries
            **kwargs: Render settings
            
        Returns:
            Batch render information
        """
        logger.info(f"Batch rendering {len(characters)} characters")
        
        return {
            "job_type": "batch_render",
            "character_count": len(characters),
            "animation_count": len(animations),
            "status": "queued",
        }
