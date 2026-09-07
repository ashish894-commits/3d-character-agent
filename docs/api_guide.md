# API Guide

## Base URL
```
http://localhost:8000/api
```

## Authentication
Currently no authentication required. For production, add OAuth2 or API keys.

## Response Format
All responses are JSON.

## Character Endpoints

### Create Character
**POST** `/character/create`

Create a new 3D character.

**Request:**
```json
{
  "name": "hero",
  "gender": "male",
  "age": 30,
  "ethnicity": "mixed",
  "height": 1.75,
  "weight": 70,
  "style": "realistic",
  "skin_tone": null,
  "hair_style": null,
  "hair_color": null,
  "clothing": null
}
```

**Response:**
```json
{
  "id": "a1b2c3d4e5f6",
  "name": "hero",
  "status": "ready",
  "params": { },
  "files": {
    "blend": "/output/characters/hero_base.blend",
    "fbx": null,
    "obj": null,
    "preview": null
  }
}
```

### Get Character
**GET** `/character/{character_id}`

Retrieve character by ID.

### List Characters
**GET** `/characters`

List all available characters.

### Delete Character
**DELETE** `/character/{character_id}`

Delete a character and its files.

## Animation Endpoints

### Generate Animation
**POST** `/animation/generate`

Generate animation for a character.

**Request:**
```json
{
  "character_id": "a1b2c3d4e5f6",
  "animation_type": "walk",
  "duration": 5.0,
  "fps": 24,
  "loop": false,
  "speed": 1.0
}
```

**Animation Types:**
- `walk` - Walking animation
- `run` - Running animation
- `dance` - Dancing animation
- `idle` - Idle/breathing animation

**Response:**
```json
{
  "character_id": "a1b2c3d4e5f6",
  "type": "walk",
  "duration": 5.0,
  "fps": 24,
  "frames": 120,
  "status": "generated"
}
```

## Rendering Endpoints

### Render Video
**POST** `/render/video`

Render character animation to video.

**Request:**
```json
{
  "character_id": "a1b2c3d4e5f6",
  "animation_type": "walk",
  "scene": "studio",
  "resolution": "1920x1080",
  "quality": "high",
  "fps": 24,
  "engine": "CYCLES",
  "samples": 256
}
```

**Quality Presets:**
- `low` - Fast, lower quality (64 samples, 1280x720)
- `medium` - Balanced (128 samples, 1920x1080)
- `high` - High quality (256 samples, 2560x1440)
- `ultra` - Maximum quality (512 samples, 3840x2160)

**Response:**
```json
{
  "character_id": "a1b2c3d4e5f6",
  "animation_type": "walk",
  "output_file": "/output/renders/a1b2c3d4e5f6_walk.mp4",
  "status": "rendering",
  "frames_total": 120,
  "duration_seconds": 5.0
}
```

### Render Preview
**POST** `/render/preview`

Quick preview render.

**Query Parameters:**
- `character_id` (required) - Character ID
- `quality` (optional) - `low` or `medium` (default: `low`)

## Video Composition Endpoints

### Compose Video
**POST** `/compose/video`

Compose rendered frames into final video.

**Request:**
```json
{
  "render_files": [
    "/output/renders/0001.png",
    "/output/renders/0002.png"
  ],
  "output_format": "mp4",
  "quality": "high",
  "fps": 24
}
```

### Add Audio
**POST** `/compose/add-audio`

Add audio track to video.

**Query Parameters:**
- `video_file` - Path to video
- `audio_file` - Path to audio

### Add Effects
**POST** `/compose/add-effects`

Apply post-processing effects.

**Request:**
```json
{
  "video_file": "/path/to/video.mp4",
  "effects": {
    "color_grade": "warm",
    "sharpen": 0.5,
    "vignette": true
  }
}
```

## Batch Processing Endpoints

### Batch Create Characters
**POST** `/batch/create-characters`

Create multiple characters in batch.

**Request:**
```json
{
  "job_type": "character_creation",
  "characters": [
    {"name": "char_1", "gender": "male"},
    {"name": "char_2", "gender": "female"}
  ],
  "animations": []
}
```

### Batch Render Videos
**POST** `/batch/render-videos`

Render multiple videos in batch.

### Get Batch Job Status
**GET** `/batch/job/{job_id}`

Check status of batch job.

## Error Responses

Errors return appropriate HTTP status codes:

- `400` - Bad Request
- `404` - Not Found
- `500` - Internal Server Error

**Error Response Format:**
```json
{
  "detail": "Error description"
}
```

## Rate Limiting

No rate limiting implemented yet. Coming in v1.0.

## Webhooks

Webhook support for job completion notifications is planned.
