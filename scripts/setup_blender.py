"""Setup scripts for Blender"""

import os
import sys
import logging
import subprocess
import zipfile
from pathlib import Path
from urllib.request import urlopen

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def download_blender(version: str = "4.0.2", target_path: str = "/opt/blender") -> bool:
    """Download and install Blender
    
    Args:
        version: Blender version to download
        target_path: Installation target path
        
    Returns:
        Success status
    """
    import platform
    
    system = platform.system().lower()
    machine = platform.machine().lower()
    
    # Map system to Blender download URL pattern
    if system == "linux":
        if "arm" in machine:
            arch = "arm64"
        else:
            arch = "x64"
        filename = f"blender-{version}-linux-{arch}.tar.xz"
    elif system == "darwin":
        arch = "arm64" if "arm" in machine else "x64"
        filename = f"blender-{version}-macos-{arch}.dmg"
    elif system == "windows":
        filename = f"blender-{version}-windows-x64.zip"
    else:
        logger.error(f"Unsupported system: {system}")
        return False
    
    url = f"https://download.blender.org/release/Blender{version.split('.')[0]}.{version.split('.')[1]}/{filename}"
    
    logger.info(f"Downloading Blender from {url}")
    
    try:
        target_path = Path(target_path)
        target_path.mkdir(parents=True, exist_ok=True)
        
        # Download file
        with urlopen(url) as response:
            total_size = int(response.headers.get('content-length', 0))
            downloaded = 0
            chunk_size = 8192
            
            download_path = target_path / filename
            with open(download_path, 'wb') as f:
                while True:
                    chunk = response.read(chunk_size)
                    if not chunk:
                        break
                    f.write(chunk)
                    downloaded += len(chunk)
                    percent = (downloaded / total_size * 100) if total_size else 0
                    print(f"Downloaded: {percent:.1f}%", end='\r')
        
        logger.info(f"Download complete: {download_path}")
        
        # Extract
        if filename.endswith('.tar.xz'):
            import tarfile
            with tarfile.open(download_path, 'r:xz') as tar:
                tar.extractall(target_path)
        elif filename.endswith('.zip'):
            with zipfile.ZipFile(download_path, 'r') as zip_ref:
                zip_ref.extractall(target_path)
        
        logger.info("Blender installed successfully")
        return True
    except Exception as e:
        logger.error(f"Error downloading Blender: {e}")
        return False


def verify_blender(blender_path: str) -> bool:
    """Verify Blender installation
    
    Args:
        blender_path: Path to Blender executable
        
    Returns:
        Success status
    """
    try:
        result = subprocess.run(
            [blender_path, "--version"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            logger.info(f"Blender verified: {result.stdout.strip()}")
            return True
        else:
            logger.error(f"Blender verification failed: {result.stderr}")
            return False
    except Exception as e:
        logger.error(f"Error verifying Blender: {e}")
        return False


def install_blender_addons(blender_path: str) -> bool:
    """Install required Blender addons
    
    Args:
        blender_path: Path to Blender executable
        
    Returns:
        Success status
    """
    logger.info("Installing Blender addons...")
    
    addon_script = """
import bpy

# Enable built-in addons
built_in_addons = [
    'io_blend_utils_shapekey_helper',
    'io_curve_svg',
    'io_image_as_planes',
    'io_mesh_ply',
    'io_mesh_uv_layout',
    'object_print3d_utils',
]

for addon in built_in_addons:
    try:
        bpy.ops.preferences.addon_enable(module=addon)
    except:
        pass

# Save preferences
bpy.ops.wm.save_userpref()
"""
    
    try:
        result = subprocess.run(
            [blender_path, "--background", "--python-expr", addon_script],
            capture_output=True,
            text=True,
            timeout=60
        )
        if result.returncode == 0:
            logger.info("Addons installed successfully")
            return True
        else:
            logger.warning(f"Addon installation warnings: {result.stderr}")
            return True  # Continue despite warnings
    except Exception as e:
        logger.error(f"Error installing addons: {e}")
        return False


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Setup Blender for 3D Character Agent")
    parser.add_argument("--version", default="4.0.2", help="Blender version")
    parser.add_argument("--path", default="/opt/blender", help="Installation path")
    parser.add_argument("--verify-only", action="store_true", help="Only verify installation")
    
    args = parser.parse_args()
    
    if args.verify_only:
        verify_blender(f"{args.path}/blender")
    else:
        if download_blender(args.version, args.path):
            blender_exe = f"{args.path}/blender"
            if verify_blender(blender_exe):
                install_blender_addons(blender_exe)
                logger.info(f"Blender setup complete at {args.path}")
            else:
                logger.error("Blender verification failed")
        else:
            logger.error("Blender download failed")
