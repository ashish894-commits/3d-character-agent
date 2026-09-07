# 3D Character Agent - Examples

## Example 1: Create a Simple Character

### Python API
```python
from src.agent import CharacterGenerator

# Initialize
gen = CharacterGenerator()

# Create character
character = gen.create(
    name="Alice",
    gender="female",
    age=25,
    height=1.65,
    weight=60,
    style="realistic",
    hair_color="brown",
    skin_tone="olive"
)

print(f"Character created: {character['id']}")
print(f"Files: {character['files']}")
```

### REST API
```bash
curl -X POST http://localhost:8000/api/character/create \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Alice",
    "gender": "female",
    "age": 25,
    "style": "realistic"
  }'
```

## Example 2: Animate a Character

### Python API
```python
from src.agent import Animator

# Load character
character = gen.load("character_id")

# Initialize animator
animator = Animator()

# Rig character
character = animator.rig_character(character)

# Generate walking animation
animation = animator.generate_animation(
    character,
    animation_type="walk",
    duration=5.0,
    fps=24,
    loop=True
)

print(f"Animation generated: {animation['frames']} frames")
```

### REST API
```bash
# Generate animation
curl -X POST http://localhost:8000/api/animation/generate \
  -H "Content-Type: application/json" \
  -d '{
    "character_id": "character_id",
    "animation_type": "walk",
    "duration": 5.0,
    "fps": 24,
    "loop": true
  }'
```

## Example 3: Render High-Quality Video

### Python API
```python
from src.agent import Renderer

# Load character and animation
character = gen.load("character_id")
animation = {...}  # Animation data

# Initialize renderer
renderer = Renderer()

# Render to video
render_info = renderer.render_to_video(
    character,
    animation,
    scene="outdoor",
    quality="ultra",
    resolution="3840x2160",
    samples=512,
    fps=24
)

print(f"Render output: {render_info['output_file']}")
```

### REST API
```bash
curl -X POST http://localhost:8000/api/render/video \
  -H "Content-Type: application/json" \
  -d '{
    "character_id": "character_id",
    "animation_type": "walk",
    "scene": "outdoor",
    "quality": "ultra",
    "resolution": "3840x2160",
    "samples": 512
  }'
```

## Example 4: Create Multiple Characters (Batch)

### Python API
```python
from src.agent import CharacterGenerator

gen = CharacterGenerator()
characters = []

# Define character specs
specs = [
    {"name": "Hero", "gender": "male", "age": 30},
    {"name": "Heroine", "gender": "female", "age": 28},
    {"name": "Villain", "gender": "male", "age": 45},
    {"name": "Elder", "gender": "male", "age": 65},
]

# Create all characters
for spec in specs:
    character = gen.create(**spec)
    characters.append(character)
    print(f"✓ Created: {character['name']}")

print(f"Total characters: {len(characters)}")
```

### REST API
```bash
curl -X POST http://localhost:8000/api/batch/create-characters \
  -H "Content-Type: application/json" \
  -d '{
    "job_type": "character_creation",
    "characters": [
      {"name": "Hero", "gender": "male", "age": 30},
      {"name": "Heroine", "gender": "female", "age": 28}
    ],
    "animations": []
  }'
```

## Example 5: Add Effects and Audio to Video

### Python API
```python
from src.agent import VideoComposer

composer = VideoComposer()

# Add effects
video_with_effects = composer.add_effects(
    video_file="/output/renders/character_walk.mp4",
    effects={
        "color_grade": "warm",
        "sharpen": 0.8,
        "vignette": True
    }
)

# Add audio
final_video = composer.add_audio(
    video_file=video_with_effects,
    audio_file="/path/to/music.mp3"
)

print(f"Final video: {final_video}")
```

### REST API
```bash
# Add effects
curl -X POST http://localhost:8000/api/compose/add-effects \
  -H "Content-Type: application/json" \
  -d '{
    "video_file": "/output/renders/character_walk.mp4",
    "effects": {
      "color_grade": "warm",
      "sharpen": 0.8,
      "vignette": true
    }
  }'

# Add audio
curl -X POST http://localhost:8000/api/compose/add-audio \
  -H "Content-Type: application/json" \
  -d '{
    "video_file": "/path/to/effects/video.mp4",
    "audio_file": "/path/to/music.mp3"
  }'
```

## Example 6: Complete Workflow

### Python Script
```python
from src.agent import CharacterGenerator, Animator, Renderer, VideoComposer
import time

# Initialize all components
gen = CharacterGenerator()
animator = Animator()
renderer = Renderer()
composer = VideoComposer()

print("=" * 60)
print("Complete 3D Character Agent Workflow")
print("=" * 60)

# Step 1: Create Character
print("\n[1] Creating character...")
character = gen.create(
    name="MainHero",
    gender="male",
    age=30,
    style="realistic"
)
print(f"✓ Character created: {character['id']}")

# Step 2: Rig Character
print("\n[2] Rigging character...")
character = animator.rig_character(character)
print("✓ Character rigged")

# Step 3: Generate Animations
print("\n[3] Generating animations...")
animations = {}
for anim_type in ["walk", "run", "idle"]:
    anim = animator.generate_animation(
        character,
        animation_type=anim_type,
        duration=5.0,
        fps=24
    )
    animations[anim_type] = anim
    print(f"✓ Generated {anim_type} animation")

# Step 4: Render Videos
print("\n[4] Rendering videos...")
for anim_type, animation in animations.items():
    render_info = renderer.render_to_video(
        character,
        animation,
        quality="high"
    )
    print(f"✓ Rendering {anim_type}...")

# Step 5: Compose Final Videos
print("\n[5] Composing final videos...")
for anim_type in animations.keys():
    compose_info = composer.compose_video(
        {"character_id": character['id'], "animation_type": anim_type},
        output_format="mp4",
        quality="high"
    )
    print(f"✓ Composed {anim_type}: {compose_info['output_file']}")

print("\n" + "=" * 60)
print("Workflow Complete!")
print("=" * 60)
```

## Example 7: List and Manage Characters

### Python API
```python
# List all characters
characters = gen.list_characters()
print(f"Total characters: {len(characters)}")

for char in characters:
    print(f"  - {char['name']} (ID: {char['id']}, Status: {char['status']})")

# Get specific character
specific_char = gen.load("character_id")
print(f"\nCharacter: {specific_char['name']}")
print(f"Age: {specific_char['params']['age']}")
print(f"Style: {specific_char['params']['style']}")

# Delete character
gen.delete("character_id")
print("✓ Character deleted")
```

### REST API
```bash
# List characters
curl http://localhost:8000/api/characters

# Get specific character
curl http://localhost:8000/api/character/a1b2c3d4e5f6

# Delete character
curl -X DELETE http://localhost:8000/api/character/a1b2c3d4e5f6
```

## Example 8: Render Preview

### Python API
```python
# Quick preview render
character = gen.load("character_id")
animation = {"character_id": character['id'], "type": "walk", "duration": 2.0, "fps": 24, "frames": 48}

preview = renderer.render_preview(
    character,
    animation,
    quality="low"  # Fast preview
)

print(f"Preview: {preview['output_file']}")
```

### REST API
```bash
curl -X POST "http://localhost:8000/api/render/preview?character_id=a1b2c3d4e5f6&quality=low"
```

## Tips & Best Practices

### Performance
- Use `quality="low"` for previews to save time
- Batch process multiple characters when possible
- Enable GPU rendering for faster results

### Quality
- Use `quality="ultra"` for final production renders
- Increase `samples` for less noisy renders
- Use higher resolution for detailed scenes

### File Management
- Output files are stored in `/output` directory
- Cache is stored in `/cache` for faster subsequent operations
- Regularly clean up old renders to save disk space

### Error Handling
```python
try:
    character = gen.load("character_id")
except FileNotFoundError:
    print("Character not found")
except Exception as e:
    print(f"Error: {e}")
```

## Integration Examples

### With Video Editing Software
```python
# Export frames for manual editing in DaVinci Resolve, Premiere, etc.
renderer.render_frames(character, animation, fps=24)
# Then import the PNG sequence into your video editor
```

### With AI Voice-Over
```python
# Generate video with character animation
video_path = renderer.render_to_video(...)

# Add AI voice-over (integration with external service)
audio_path = generate_voiceover("Hello, I am a 3D character!")

# Combine video and audio
final_video = composer.add_audio(video_path, audio_path)
```

### Webhook Notifications
```python
# Coming in future versions
# Subscribe to render completion events
renderer.on_render_complete(callback=my_callback_function)
```

## Troubleshooting

### Character Creation Fails
- Check if MakeHuman is properly installed
- Verify paths in `.env` file
- Check system memory availability

### Animation Issues
- Ensure character is properly rigged
- Check animation duration and frame count
- Verify keyframe data

### Render Takes Too Long
- Reduce sample count
- Decrease resolution
- Use `quality="low"` or `quality="medium"`
- Enable GPU rendering

### Memory Errors
- Reduce batch size
- Lower resolution
- Restart the service

For more help, check the [API Guide](api_guide.md) or [Installation Guide](installation.md).
