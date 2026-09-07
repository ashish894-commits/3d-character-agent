"""Configuration settings and environment variables"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings:
    """Application settings"""
    
    # Base paths
    BASE_DIR = Path(__file__).parent.parent.parent
    OUTPUT_DIR = Path(os.getenv("OUTPUT_DIR", "./output"))
    CACHE_DIR = Path(os.getenv("CACHE_DIR", "./cache"))
    TEMP_DIR = Path(os.getenv("TEMP_DIR", "/tmp/3d-agent"))
    
    # Create directories if they don't exist
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    TEMP_DIR.mkdir(parents=True, exist_ok=True)
    
    # Blender settings
    BLENDER_PATH = os.getenv("BLENDER_PATH", "blender")
    BLENDER_PYTHON = os.getenv("BLENDER_PYTHON", "")
    BLENDER_GPU_ENABLED = os.getenv("BLENDER_GPU_ENABLED", "true").lower() == "true"
    BLENDER_GPU_TYPE = os.getenv("BLENDER_GPU_TYPE", "CUDA")  # CUDA, OPTIX, HIP
    
    # Rendering settings
    RENDER_ENGINE = os.getenv("RENDER_ENGINE", "CYCLES")  # CYCLES or EEVEE
    RENDER_SAMPLES = int(os.getenv("RENDER_SAMPLES", "256"))
    RENDER_RESOLUTION = os.getenv("RENDER_RESOLUTION", "1920x1080")
    RENDER_FORMAT = os.getenv("RENDER_FORMAT", "PNG")
    
    # API settings
    API_HOST = os.getenv("API_HOST", "0.0.0.0")
    API_PORT = int(os.getenv("API_PORT", "8000"))
    API_DEBUG = os.getenv("API_DEBUG", "false").lower() == "true"
    API_WORKERS = int(os.getenv("API_WORKERS", "4"))
    
    # Performance settings
    MAX_WORKERS = int(os.getenv("MAX_WORKERS", "4"))
    BATCH_SIZE = int(os.getenv("BATCH_SIZE", "2"))
    GPU_MEMORY = os.getenv("GPU_MEMORY", "8GB")
    
    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = OUTPUT_DIR / "app.log"
