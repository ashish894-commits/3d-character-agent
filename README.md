# 3D Character Agent 🎬🎨

An AI-powered agent for creating 3D animated characters and cinematic videos using open-source tools and platforms.

## Features

✨ **Core Capabilities**
- **Automated 3D Character Creation** - Generate customizable 3D human characters
- **AI-Driven Animation** - Physics-based character rigging and motion
- **Cinematic Rendering** - High-quality 3D renders with lighting and effects
- **Video Composition** - Automatic video editing and scene composition
- **Batch Processing** - Create multiple characters and videos in sequence
- **API Integration** - RESTful API for programmatic control

## Tech Stack

### Open Source Platforms
- **Blender** (4.0+) - 3D modeling, animation, rendering, and video editing
- **MakeHuman** - Rapid human character creation and customization
- **Cascadeur** - AI-assisted character animation and physics
- **OpenCV** - Video processing and composition
- **FFmpeg** - Video encoding and format conversion

### Python Ecosystem
- `bpy` - Blender Python API
- `Flask/FastAPI` - REST API server
- `Pillow` - Image processing
- `numpy/scipy` - Numerical computing
- `pydantic` - Data validation

## Project Structure

```
3d-character-agent/
├── src/
│   ├── agent/
│   │   ├── __init__.py
│   │   ├── character_generator.py      # Character creation pipeline
│   │   ├── animator.py                 # Animation and rigging
│   │   ├── renderer.py                 # Rendering engine
│   │   └── video_composer.py           # Video editing and composition
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routes.py                   # API endpoints
│   │   ├── models.py                   # Pydantic models
│   │   └── server.py                   # FastAPI application
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── blender_scripts.py          # Blender integration
│   │   ├── makehuman_scripts.py        # MakeHuman integration
│   │   └── ffmpeg_wrapper.py           # FFmpeg utilities
│   └── config/
│       ├── __init__.py
│       └── settings.py                 # Configuration management
├── scripts/
│   ├── setup_blender.py                # Install Blender dependencies
│   ├── setup_makehuman.py              # Setup MakeHuman
│   └── demo_workflow.py                # Example workflow
├── tests/
│   ├── test_agent.py
│   ├── test_api.py
│   └── test_renderer.py
├── docs/
│   ├── installation.md
│   ├── api_guide.md
│   └── examples.md
├── requirements.txt
├── setup.py
└── docker-compose.yml
```

## Installation

### Prerequisites
- Python 3.8+
- Blender 4.0+ (downloadable automatically)
- FFmpeg
- Docker (optional)

### Quick Start

```bash
# Clone the repository
git clone https://github.com/ashish894-commits/3d-character-agent.git
cd 3d-character-agent

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run setup
python scripts/setup_blender.py
python scripts/setup_makehuman.py

# Start the API server
python -m src.api.server
```

### Docker Deployment

```bash
docker-compose up -d
```

## Usage

### API Endpoints

#### Create a Character
```bash
curl -X POST http://localhost:8000/api/character/create \
  -H "Content-Type: application/json" \
  -d '{
    "name": "hero",
    "gender": "male",
    "age": 30,
    "style": "realistic"
  }'
```

#### Generate Animation
```bash
curl -X POST http://localhost:8000/api/animation/generate \
  -H "Content-Type: application/json" \
  -d '{
    "character_id": "hero_001",
    "animation_type": "walk",
    "duration": 5,
    "fps": 24
  }'
```

#### Render Video
```bash
curl -X POST http://localhost:8000/api/render/video \
  -H "Content-Type: application/json" \
  -d '{
    "character_id": "hero_001",
    "scene": "outdoor",
    "resolution": "1920x1080",
    "quality": "high"
  }'
```

### Python API

```python
from src.agent import CharacterGenerator, Animator, Renderer

# Create character
generator = CharacterGenerator()
character = generator.create(
    name="Emma",
    gender="female",
    age=28,
    style="stylized"
)

# Animate character
animator = Animator()
animator.rig_character(character)
animation = animator.generate_animation(
    character,
    animation_type="dance",
    duration=10
)

# Render to video
renderer = Renderer()
video = renderer.render_to_video(
    character,
    animation,
    scene="studio",
    quality="4k"
)
```

## Workflow

```
1. Character Generation
   ├── Define parameters (gender, age, style, etc.)
   ├── Generate base model (MakeHuman/Blender)
   ├── Apply customizations (clothing, hair, etc.)
   └── Export model

2. Rigging & Preparation
   ├── Auto-rig character (Armature)
   ├── Add materials and textures
   ├── Setup IK constraints
   └── Prepare for animation

3. Animation
   ├── Load motion capture data (optional)
   ├── Apply keyframe animation
   ├── Use physics simulation
   ├── Add facial expressions
   └── Refine motion

4. Scene Setup
   ├── Create/load environment
   ├── Position character
   ├── Setup lighting
   └── Configure camera

5. Rendering
   ├── Configure render settings
   ├── Render frames
   ├── Apply post-processing
   └── Generate output

6. Video Composition
   ├── Composite multiple layers
   ├── Add effects and transitions
   ├── Apply audio/music
   └── Encode to video format
```

## Configuration

Create `config.env` in the project root:

```env
# Blender Settings
BLENDER_PATH=/opt/blender/blender
BLENDER_PYTHON=/opt/blender/python/bin/python
BLENDER_GPU_ENABLED=true
BLENDER_GPU_TYPE=CUDA

# Rendering
RENDER_ENGINE=CYCLES
RENDER_SAMPLES=256
RENDER_RESOLUTION=1920x1080
RENDER_FORMAT=PNG

# API
API_HOST=0.0.0.0
API_PORT=8000
API_DEBUG=false

# Storage
OUTPUT_DIR=./output
CACHE_DIR=./cache
TEMP_DIR=/tmp/3d-agent

# Performance
MAX_WORKERS=4
BATCH_SIZE=2
GPU_MEMORY=8GB
```

## Key Components

### Character Generator
Generates diverse 3D human characters with customizable features:
- Body parameters (height, weight, proportions)
- Facial features (age, gender, ethnicity)
- Clothing and accessories
- Hair styles and colors
- Skin texture variations

### Animator
Handles character rigging and animation:
- Automatic bone rigging
- Motion capture integration
- Keyframe animation
- Physics-based movement
- Facial animation

### Renderer
Produces high-quality 3D output:
- Multiple render engines (Cycles, Eevee)
- Lighting setups (3-point lighting, HDRI)
- Material and texture application
- Post-processing effects
- Real-time preview

### Video Composer
Assembles final videos:
- Multi-layer composition
- Transitions and effects
- Audio synchronization
- Color grading
- Format encoding (MP4, ProRes, etc.)

## Examples

### Create a Walking Character
```python
from src.agent import CharacterGenerator, Animator, Renderer

# Generate character
gen = CharacterGenerator()
char = gen.create(name="walker", gender="male", age=25)

# Add walking animation
animator = Animator()
animator.rig_character(char)
anim = animator.generate_animation(char, "walk", duration=5)

# Render video
renderer = Renderer()
video = renderer.render_to_video(char, anim)
print(f"Video saved: {video.path}")
```

### Batch Create Multiple Characters
```python
from src.agent import CharacterGenerator

gen = CharacterGenerator()
characters = []
for i in range(10):
    char = gen.create(name=f"char_{i}", random_style=True)
    characters.append(char)
print(f"Created {len(characters)} characters")
```

## Performance Optimization

- **GPU Rendering**: Supports CUDA, OptiX, and HIP acceleration
- **Multi-threading**: Parallel processing of characters and frames
- **Caching**: Intelligent caching of models and scenes
- **Streaming**: Real-time preview and progressive rendering

## Contributing

We welcome contributions! Please:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## Roadmap

- [ ] Motion capture integration
- [ ] Real-time face capture
- [ ] Advanced cloth simulation
- [ ] Crowd simulation
- [ ] VR/360° video support
- [ ] WebGL viewer
- [ ] Cloud rendering support
- [ ] AI-driven dialogue animation

## Troubleshooting

### Blender not found
```bash
python scripts/setup_blender.py --path /custom/blender/path
```

### GPU rendering not working
```bash
# Check GPU support
blender --version
# Rebuild with GPU support
python scripts/setup_blender.py --gpu cuda
```

### Out of memory errors
```env
# Reduce resolution or samples
RENDER_SAMPLES=64
RENDER_RESOLUTION=1280x720
```

## License

Apache License 2.0 - See LICENSE file for details

## Support

- 📖 [Documentation](docs/)
- 🐛 [Issue Tracker](https://github.com/ashish894-commits/3d-character-agent/issues)
- 💬 [Discussions](https://github.com/ashish894-commits/3d-character-agent/discussions)

## Acknowledgments

Built on top of:
- [Blender](https://www.blender.org/) - 3D Creation Suite
- [MakeHuman](http://www.makehumancommunity.org/) - Character Creator
- [Cascadeur](https://cascadeur.com/) - Animation Tool
- Open source community

---

**Status**: 🚀 In Active Development

**Last Updated**: 2025

**Author**: Ashish Kumar (ashish894-commits)
