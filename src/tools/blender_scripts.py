"""Blender integration utilities"""

import subprocess
import logging
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


class BlenderScripts:
    """Blender Python scripts for automation"""
    
    @staticmethod
    def get_character_rigging_script(character_path: str) -> str:
        """Get script for rigging a character"""
        return f"""
import bpy
import bmesh
from mathutils import Vector

# Load character
bpy.ops.wm.open_mainfile(filepath=r'{character_path}')

# Get mesh object
mesh_obj = None
for obj in bpy.data.objects:
    if obj.type == 'MESH':
        mesh_obj = obj
        break

if mesh_obj:
    # Create armature
    bpy.ops.object.armature_add(location=(0, 0, 1))
    armature_obj = bpy.context.active_object
    armature_obj.name = "Armature"
    
    # Enter edit mode
    bpy.context.view_layer.objects.active = armature_obj
    bpy.ops.object.mode_set(mode='EDIT')
    
    # Get armature data
    arm_data = armature_obj.data
    
    # Create bones (simplified humanoid skeleton)
    bone_positions = {{
        'Pelvis': (0, 0, 0),
        'Spine': (0, 0, 0.15),
        'Chest': (0, 0, 0.35),
        'Neck': (0, 0, 0.55),
        'Head': (0, 0, 0.7),
    }}
    
    # Parent mesh to armature
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.context.view_layer.objects.active = mesh_obj
    mesh_obj.select_set(True)
    bpy.context.view_layer.objects.active = armature_obj
    bpy.ops.object.parent_set(type='ARMATURE_AUTO')
    
    # Save
    bpy.ops.wm.save_mainfile()
"""
    
    @staticmethod
    def get_render_script(blender_path: str, output_path: str,
                         render_settings: dict) -> str:
        """Get script for rendering"""
        return f"""
import bpy
import os

# Load scene
bpy.ops.wm.open_mainfile(filepath=r'{blender_path}')

# Set render settings
scene = bpy.context.scene
scene.render.engine = '{render_settings.get("engine", "CYCLES")}'
scene.render.resolution_x = {render_settings.get("resolution_x", 1920)}
scene.render.resolution_y = {render_settings.get("resolution_y", 1080)}
scene.render.fps = {render_settings.get("fps", 24)}

# Configure cycles
bpy.context.scene.cycles.samples = {render_settings.get("samples", 256)}
bpy.context.scene.cycles.use_denoising = True
bpy.context.scene.cycles.denoiser = '{render_settings.get("denoiser", "OptiX")}'

# GPU rendering
bpy.context.preferences.addons['cycles'].preferences.compute_device_type = 'CUDA'
for device in bpy.context.preferences.addons['cycles'].preferences.devices:
    device.use = True

# Output settings
scene.render.filepath = r'{output_path}'
scene.render.image_settings.file_format = 'PNG'

# Render animation
scene.frame_start = 0
scene.frame_end = {render_settings.get("frames", 240)}
bpy.ops.render.render(animation=True, write_still=True)
"""
    
    @staticmethod
    def get_material_setup_script(style: str) -> str:
        """Get script for setting up materials"""
        if style == "realistic":
            return """
import bpy
from bpy.types import ShaderNodeBsdfPrincipled

# Setup realistic skin material
for obj in bpy.context.scene.objects:
    if obj.type == 'MESH':
        mat = bpy.data.materials.new(name="Skin")
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes["Principled BSDF"]
        bsdf.inputs["Base Color"].default_value = (0.8, 0.7, 0.65, 1.0)
        bsdf.inputs["Roughness"].default_value = 0.3
        bsdf.inputs["Subsurface Weight"].default_value = 0.1
        obj.data.materials.append(mat)
"""
        elif style == "stylized":
            return """
import bpy

# Setup stylized material with toon shading
for obj in bpy.context.scene.objects:
    if obj.type == 'MESH':
        mat = bpy.data.materials.new(name="Stylized")
        mat.use_nodes = True
        # Add toon shader nodes
"""
        else:
            return """
import bpy

# Default material setup
for obj in bpy.context.scene.objects:
    if obj.type == 'MESH':
        mat = bpy.data.materials.new(name="Default")
        obj.data.materials.append(mat)
"""


def run_blender_script(blender_path: str, script: str,
                      background: bool = True) -> bool:
    """Execute Blender Python script
    
    Args:
        blender_path: Path to Blender executable
        script: Python script to execute
        background: Run in background mode
        
    Returns:
        Success status
    """
    try:
        cmd = [blender_path]
        if background:
            cmd.append("--background")
        cmd.extend(["--python-expr", script])
        
        logger.info(f"Running Blender script: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            logger.error(f"Blender error: {result.stderr}")
            return False
        
        logger.info("Blender script executed successfully")
        return True
    except Exception as e:
        logger.error(f"Error running Blender script: {e}")
        return False
