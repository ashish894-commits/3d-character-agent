"""3D Character Agent - AI-powered 3D character creation and animation"""

__version__ = "0.1.0"
__author__ = "Ashish Kumar"
__email__ = "ashish.894@yahoo.com"

from .agent.character_generator import CharacterGenerator
from .agent.animator import Animator
from .agent.renderer import Renderer
from .agent.video_composer import VideoComposer

__all__ = [
    "CharacterGenerator",
    "Animator",
    "Renderer",
    "VideoComposer",
]
