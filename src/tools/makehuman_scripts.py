"""MakeHuman integration utilities"""

import subprocess
import logging
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


class MakeHumanScripts:
    """MakeHuman Python scripts for character generation"""
    
    @staticmethod
    def get_character_generation_script(params: dict, output_path: str) -> str:
        """Get script for generating character"""
        return f"""
import gui3d
import mh
from core import G

# Create new human
G.app.resetHuman()
human = G.app.selectedHuman

# Set parameters
human.getHeightTarget().setValue({params.get('height', 1.75)})
human.getAgeValue().setValue({params.get('age', 30) / 100.0})

# Set gender
if '{params.get('gender', 'male')}' == 'female':
    human.genderValue = 1.0
else:
    human.genderValue = 0.0

# Set ethnicity
ethnicity_map = {{
    'african': 0.7,
    'asian': 0.3,
    'caucasian': 0.0,
    'mixed': 0.5,
}}
if 'ethnicity' in {params}:
    ethnic_val = ethnicity_map.get('{params.get('ethnicity', 'mixed')}', 0.5)
    # Apply ethnicity modifiers

# Export as Blender file
G.app.selectedHuman.export(r'{output_path}')
"""
    
    @staticmethod
    def get_clothing_script(clothing_type: str) -> str:
        """Get script for applying clothing"""
        clothing_map = {
            "casual": "clothes/casualoutfit.mhclo",
            "formal": "clothes/formalwear.mhclo",
            "athletic": "clothes/sportswear.mhclo",
            "fantasy": "clothes/fantasy_outfit.mhclo",
        }
        
        clothing_path = clothing_map.get(clothing_type, "clothes/default.mhclo")
        
        return f"""
import gui3d
from core import G
import os

# Load clothing
clothing_file = r'{clothing_path}'
if os.path.exists(clothing_file):
    G.app.selectedHuman.loadClothing(clothing_file)
"""


def run_makehuman_script(makehuman_path: str, script: str) -> bool:
    """Execute MakeHuman Python script
    
    Args:
        makehuman_path: Path to MakeHuman executable
        script: Python script to execute
        
    Returns:
        Success status
    """
    try:
        cmd = [makehuman_path, "--batch", "--script", script]
        logger.info(f"Running MakeHuman script")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            logger.error(f"MakeHuman error: {result.stderr}")
            return False
        
        logger.info("MakeHuman script executed successfully")
        return True
    except Exception as e:
        logger.error(f"Error running MakeHuman script: {e}")
        return False
