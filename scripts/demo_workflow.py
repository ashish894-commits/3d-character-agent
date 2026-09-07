"""Demo workflow for 3D Character Agent"""

import sys
import logging
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.agent import CharacterGenerator, Animator, Renderer, VideoComposer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def demo_workflow():
    """Run a complete demo workflow"""
    
    logger.info("\n" + "="*60)
    logger.info("3D Character Agent - Demo Workflow")
    logger.info("="*60 + "\n")
    
    # Initialize components
    logger.info("Initializing components...")
    char_gen = CharacterGenerator()
    animator = Animator()
    renderer = Renderer()
    composer = VideoComposer()
    
    # Step 1: Create Character
    logger.info("\n[STEP 1] Creating a 3D character...")
    character = char_gen.create(
        name="hero_001",
        gender="male",
        age=30,
        style="realistic",
        height=1.80,
        weight=75,
    )
    logger.info(f"✓ Character created: {character['id']}")
    logger.info(f"  Name: {character['name']}")
    logger.info(f"  Status: {character['status']}")
    
    # Step 2: Rig Character
    logger.info("\n[STEP 2] Rigging character for animation...")
    character = animator.rig_character(character)
    logger.info(f"✓ Character rigged successfully")
    logger.info(f"  Armature: {character.get('armature', 'N/A')}")
    
    # Step 3: Generate Animation
    logger.info("\n[STEP 3] Generating walking animation...")
    animation = animator.generate_animation(
        character,
        animation_type="walk",
        duration=5.0,
        fps=24,
    )
    logger.info(f"✓ Animation generated: {animation['type']}")
    logger.info(f"  Duration: {animation['duration']} seconds")
    logger.info(f"  Total frames: {animation['frames']}")
    logger.info(f"  Keyframes created: {len(animation['keyframes'])}")
    
    # Step 4: Render Video
    logger.info("\n[STEP 4] Rendering to video...")
    render_info = renderer.render_to_video(
        character,
        animation,
        scene="studio",
        quality="high",
        resolution="1920x1080",
        samples=256,
    )
    logger.info(f"✓ Render job initiated")
    logger.info(f"  Output: {render_info['output_file']}")
    logger.info(f"  Quality: {render_info['settings']['quality']}")
    logger.info(f"  Resolution: {render_info['settings']['resolution']}")
    
    # Step 5: Video Composition
    logger.info("\n[STEP 5] Composing final video...")
    compose_info = composer.compose_video(
        render_info,
        output_format="mp4",
        quality="high",
    )
    logger.info(f"✓ Video composed")
    logger.info(f"  Output: {compose_info['output_file']}")
    logger.info(f"  Format: {compose_info['format']}")
    
    # Summary
    logger.info("\n" + "="*60)
    logger.info("Demo Workflow Complete!")
    logger.info("="*60)
    logger.info(f"\nGenerated Assets:")
    logger.info(f"  Character ID: {character['id']}")
    logger.info(f"  Character File: {character['files']['blend']}")
    logger.info(f"  Animation Type: {animation['type']}")
    logger.info(f"  Video Output: {compose_info['output_file']}")
    logger.info(f"\nNext Steps:")
    logger.info(f"  1. Check the output directory for generated files")
    logger.info(f"  2. Review the rendered video")
    logger.info(f"  3. Customize and create more characters")
    logger.info(f"  4. Explore batch processing for multiple videos")
    logger.info("\n")


def demo_batch_processing():
    """Demo batch character and animation generation"""
    
    logger.info("\n" + "="*60)
    logger.info("3D Character Agent - Batch Processing Demo")
    logger.info("="*60 + "\n")
    
    char_gen = CharacterGenerator()
    animator = Animator()
    renderer = Renderer()
    
    # Create multiple characters
    logger.info("Creating 5 characters...")
    characters = []
    for i in range(5):
        char = char_gen.create(
            name=f"character_{i:02d}",
            gender="male" if i % 2 == 0 else "female",
            age=20 + (i * 5),
            style="realistic",
        )
        characters.append(char)
        logger.info(f"  ✓ Created: {char['name']} (ID: {char['id']})")
    
    # Generate animations for each
    logger.info("\nGenerating animations...")
    animations = []
    for i, char in enumerate(characters):
        animator.rig_character(char)
        anim = animator.generate_animation(
            char,
            animation_type="walk" if i % 2 == 0 else "dance",
            duration=5.0,
        )
        animations.append(anim)
        logger.info(f"  ✓ Generated {anim['type']} for {char['name']}")
    
    logger.info(f"\n✓ Batch processing complete: {len(characters)} characters, {len(animations)} animations")
    logger.info("\n")


if __name__ == "__main__":
    try:
        # Run main demo
        demo_workflow()
        
        # Run batch demo
        demo_batch_processing()
        
    except Exception as e:
        logger.error(f"Demo failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
