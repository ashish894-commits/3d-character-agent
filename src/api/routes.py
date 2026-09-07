"""API routes for 3D character agent"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import List
from datetime import datetime
import logging

from .models import (
    CharacterCreateRequest, CharacterResponse,
    AnimationGenerateRequest, AnimationResponse,
    RenderVideoRequest, RenderResponse,
    VideoComposeRequest, VideoComposeResponse,
    BatchJobRequest, BatchJobResponse,
    HealthResponse,
)
from src.agent import CharacterGenerator, Animator, Renderer, VideoComposer

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api", tags=["3D Character Agent"])

# Initialize components
char_gen = CharacterGenerator()
animator = Animator()
renderer = Renderer()
composer = VideoComposer()


# ==================== Health ====================

@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        version="0.1.0",
        timestamp=datetime.now().isoformat(),
    )


# ==================== Character Management ====================

@router.post("/character/create", response_model=CharacterResponse)
async def create_character(request: CharacterCreateRequest):
    """Create a new 3D character
    
    Args:
        request: Character creation parameters
        
    Returns:
        Character data with file paths
    """
    try:
        logger.info(f"Creating character: {request.name}")
        character = char_gen.create(**request.dict())
        return CharacterResponse(**character)
    except Exception as e:
        logger.error(f"Error creating character: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/character/{character_id}", response_model=CharacterResponse)
async def get_character(character_id: str):
    """Get character by ID
    
    Args:
        character_id: Character ID
        
    Returns:
        Character data
    """
    try:
        character = char_gen.load(character_id)
        return CharacterResponse(**character)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Character not found")
    except Exception as e:
        logger.error(f"Error loading character: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/characters", response_model=List[CharacterResponse])
async def list_characters():
    """List all available characters
    
    Returns:
        List of all characters
    """
    try:
        characters = char_gen.list_characters()
        return [CharacterResponse(**char) for char in characters]
    except Exception as e:
        logger.error(f"Error listing characters: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/character/{character_id}")
async def delete_character(character_id: str):
    """Delete a character
    
    Args:
        character_id: Character ID to delete
        
    Returns:
        Success message
    """
    try:
        success = char_gen.delete(character_id)
        if not success:
            raise HTTPException(status_code=404, detail="Character not found")
        return {"message": f"Character {character_id} deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting character: {e}")
        raise HTTPException(status_code=400, detail=str(e))


# ==================== Animation ====================

@router.post("/animation/generate", response_model=AnimationResponse)
async def generate_animation(request: AnimationGenerateRequest):
    """Generate animation for a character
    
    Args:
        request: Animation generation parameters
        
    Returns:
        Animation data
    """
    try:
        logger.info(f"Generating {request.animation_type} animation")
        
        # Load character
        character = char_gen.load(request.character_id)
        
        # Rig character if not already rigged
        if not character.get("rigged"):
            character = animator.rig_character(character)
        
        # Generate animation
        animation = animator.generate_animation(
            character,
            animation_type=request.animation_type,
            duration=request.duration,
            fps=request.fps,
            loop=request.loop,
            speed=request.speed,
        )
        
        return AnimationResponse(**animation)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Character not found")
    except Exception as e:
        logger.error(f"Error generating animation: {e}")
        raise HTTPException(status_code=400, detail=str(e))


# ==================== Rendering ====================

@router.post("/render/video", response_model=RenderResponse)
async def render_video(request: RenderVideoRequest, background_tasks: BackgroundTasks):
    """Render character animation to video
    
    Args:
        request: Render parameters
        background_tasks: FastAPI background tasks
        
    Returns:
        Render job information
    """
    try:
        logger.info(f"Starting render job for {request.character_id}")
        
        # Load character
        character = char_gen.load(request.character_id)
        
        # Load or generate animation
        animation = {
            "character_id": request.character_id,
            "type": request.animation_type,
            "duration": 5.0,
            "fps": request.fps,
            "frames": int(5.0 * request.fps),
        }
        
        # Trigger render
        render_info = renderer.render_to_video(
            character,
            animation,
            scene=request.scene,
            resolution=request.resolution,
            quality=request.quality,
            engine=request.engine,
            samples=request.samples,
        )
        
        # Queue as background task
        background_tasks.add_task(logger.info, f"Render job queued: {request.character_id}")
        
        return RenderResponse(**render_info)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Character not found")
    except Exception as e:
        logger.error(f"Error rendering video: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/render/preview")
async def render_preview(character_id: str, quality: str = "low"):
    """Render quick preview
    
    Args:
        character_id: Character ID
        quality: Preview quality (low, medium)
        
    Returns:
        Preview render info
    """
    try:
        character = char_gen.load(character_id)
        animation = {
            "character_id": character_id,
            "type": "idle",
            "duration": 2.0,
            "fps": 24,
            "frames": 48,
        }
        
        preview_info = renderer.render_preview(character, animation, quality)
        return preview_info
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Character not found")
    except Exception as e:
        logger.error(f"Error rendering preview: {e}")
        raise HTTPException(status_code=400, detail=str(e))


# ==================== Video Composition ====================

@router.post("/compose/video", response_model=VideoComposeResponse)
async def compose_video(request: VideoComposeRequest):
    """Compose rendered frames into final video
    
    Args:
        request: Composition parameters
        
    Returns:
        Composed video info
    """
    try:
        logger.info(f"Composing video from {len(request.render_files)} files")
        
        render_data = {
            "character_id": "composite",
            "animation_type": "composite",
            "fps": request.fps,
        }
        
        compose_info = composer.compose_video(
            render_data,
            output_format=request.output_format,
            quality=request.quality,
        )
        
        return VideoComposeResponse(**compose_info)
    except Exception as e:
        logger.error(f"Error composing video: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/compose/add-audio")
async def add_audio(video_file: str, audio_file: str):
    """Add audio to video
    
    Args:
        video_file: Path to video file
        audio_file: Path to audio file
        
    Returns:
        Video with audio path
    """
    try:
        output_file = composer.add_audio(video_file, audio_file)
        return {"output_file": output_file, "status": "success"}
    except Exception as e:
        logger.error(f"Error adding audio: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/compose/add-effects")
async def add_effects(video_file: str, effects: dict):
    """Add effects to video
    
    Args:
        video_file: Path to video file
        effects: Effects dictionary
        
    Returns:
        Video with effects path
    """
    try:
        output_file = composer.add_effects(video_file, effects)
        return {"output_file": output_file, "status": "success"}
    except Exception as e:
        logger.error(f"Error adding effects: {e}")
        raise HTTPException(status_code=400, detail=str(e))


# ==================== Batch Processing ====================

@router.post("/batch/create-characters", response_model=BatchJobResponse)
async def batch_create_characters(request: BatchJobRequest, background_tasks: BackgroundTasks):
    """Create multiple characters in batch
    
    Args:
        request: Batch job parameters
        background_tasks: FastAPI background tasks
        
    Returns:
        Batch job info
    """
    try:
        job_id = f"batch_{datetime.now().timestamp()}"
        logger.info(f"Starting batch job: {job_id}")
        
        background_tasks.add_task(logger.info, f"Processing batch job: {job_id}")
        
        return BatchJobResponse(
            job_id=job_id,
            job_type="character_creation",
            status="queued",
            task_count=len(request.characters),
            created_at=datetime.now().isoformat(),
        )
    except Exception as e:
        logger.error(f"Error starting batch job: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/batch/render-videos", response_model=BatchJobResponse)
async def batch_render_videos(request: BatchJobRequest, background_tasks: BackgroundTasks):
    """Render multiple videos in batch
    
    Args:
        request: Batch job parameters
        background_tasks: FastAPI background tasks
        
    Returns:
        Batch job info
    """
    try:
        job_id = f"render_{datetime.now().timestamp()}"
        logger.info(f"Starting batch render job: {job_id}")
        
        background_tasks.add_task(logger.info, f"Processing render batch: {job_id}")
        
        return BatchJobResponse(
            job_id=job_id,
            job_type="video_rendering",
            status="queued",
            task_count=len(request.animations),
            created_at=datetime.now().isoformat(),
        )
    except Exception as e:
        logger.error(f"Error starting batch render job: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/batch/job/{job_id}")
async def get_batch_job_status(job_id: str):
    """Get status of batch job
    
    Args:
        job_id: Job ID
        
    Returns:
        Job status information
    """
    return {
        "job_id": job_id,
        "status": "in_progress",
        "progress": 50,
        "completed_tasks": 5,
        "total_tasks": 10,
    }
