"""Pydantic models for API requests and responses"""

from typing import Optional, List
from pydantic import BaseModel, Field


class CharacterCreateRequest(BaseModel):
    """Request to create a character"""
    name: str = Field(..., description="Character name")
    gender: str = Field("male", description="Character gender")
    age: int = Field(30, description="Character age")
    ethnicity: str = Field("mixed", description="Character ethnicity")
    height: float = Field(1.75, description="Height in meters")
    weight: float = Field(70, description="Weight in kg")
    style: str = Field("realistic", description="Character style")
    skin_tone: Optional[str] = Field(None, description="Skin tone")
    hair_style: Optional[str] = Field(None, description="Hair style")
    hair_color: Optional[str] = Field(None, description="Hair color")
    clothing: Optional[str] = Field(None, description="Clothing type")


class CharacterResponse(BaseModel):
    """Response containing character data"""
    id: str
    name: str
    status: str
    params: dict
    files: dict


class AnimationGenerateRequest(BaseModel):
    """Request to generate animation"""
    character_id: str = Field(..., description="Character ID")
    animation_type: str = Field(..., description="Type of animation")
    duration: float = Field(5.0, description="Duration in seconds")
    fps: int = Field(24, description="Frames per second")
    loop: bool = Field(False, description="Loop animation")
    speed: float = Field(1.0, description="Playback speed")


class AnimationResponse(BaseModel):
    """Response containing animation data"""
    character_id: str
    type: str
    duration: float
    fps: int
    frames: int
    status: str


class RenderVideoRequest(BaseModel):
    """Request to render video"""
    character_id: str = Field(..., description="Character ID")
    animation_type: str = Field("walk", description="Animation type")
    scene: Optional[str] = Field(None, description="Scene name")
    resolution: str = Field("1920x1080", description="Resolution")
    quality: str = Field("high", description="Quality preset")
    fps: int = Field(24, description="Frames per second")
    engine: str = Field("CYCLES", description="Render engine")
    samples: int = Field(256, description="Render samples")


class RenderResponse(BaseModel):
    """Response containing render data"""
    character_id: str
    animation_type: str
    output_file: str
    status: str
    frames_total: int
    duration_seconds: float


class VideoComposeRequest(BaseModel):
    """Request to compose video"""
    render_files: List[str] = Field(..., description="List of render file paths")
    output_format: str = Field("mp4", description="Output format")
    quality: str = Field("high", description="Quality preset")
    fps: int = Field(24, description="Frames per second")


class VideoComposeResponse(BaseModel):
    """Response containing composed video data"""
    output_file: str
    format: str
    quality: str
    status: str


class BatchJobRequest(BaseModel):
    """Request for batch processing"""
    job_type: str = Field(..., description="Job type")
    characters: List[dict] = Field(..., description="Character specifications")
    animations: List[dict] = Field(..., description="Animation specifications")


class BatchJobResponse(BaseModel):
    """Response containing batch job info"""
    job_id: str
    job_type: str
    status: str
    task_count: int
    created_at: str


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    version: str
    timestamp: str
