"""Documentation - Installation Guide"""

# Installation Guide

## System Requirements

- **OS**: Windows 10+, macOS 10.13+, or Linux (Ubuntu 20.04+)
- **Python**: 3.8 or higher
- **RAM**: 16GB minimum (32GB recommended)
- **GPU**: NVIDIA GPU with CUDA support (optional but recommended)
- **Disk Space**: 50GB+ for Blender, MakeHuman, and output files

## Step 1: Clone Repository

```bash
git clone https://github.com/ashish894-commits/3d-character-agent.git
cd 3d-character-agent
```

## Step 2: Create Virtual Environment

```bash
# Linux/macOS
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

## Step 3: Install Python Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## Step 4: Setup Blender

### Automatic Setup (Recommended)
```bash
python scripts/setup_blender.py --version 4.0.2 --path /opt/blender
```

### Manual Setup
1. Download Blender from https://www.blender.org/download/
2. Install to `/opt/blender` (Linux/macOS) or `C:\\Program Files\\Blender` (Windows)
3. Verify installation:
   ```bash
   blender --version
   ```

## Step 5: Setup MakeHuman

### Automatic Setup
```bash
python scripts/setup_makehuman.py --version 1.2.0 --path /opt/makehuman
```

### Manual Setup
1. Download from http://www.makehumancommunity.org/downloads.html
2. Extract to `/opt/makehuman` or preferred location
3. Note the installation path for configuration

## Step 6: Install FFmpeg

### Linux (Ubuntu/Debian)
```bash
sudo apt-get install ffmpeg
```

### macOS
```bash
brew install ffmpeg
```

### Windows
Download from https://ffmpeg.org/download.html or use Chocolatey:
```bash
choco install ffmpeg
```

## Step 7: Configure Environment

```bash
# Copy example config
cp .env.example .env

# Edit .env with your paths
nano .env
```

Update these key variables:
```env
BLENDER_PATH=/opt/blender/blender
BLENDER_GPU_ENABLED=true
BLENDER_GPU_TYPE=CUDA
RENDER_SAMPLES=256
```

## Step 8: Verify Installation

```bash
# Test Blender
python scripts/setup_blender.py --verify-only

# Run demo
python scripts/demo_workflow.py
```

## Step 9: Start API Server

```bash
python -m src.api.server
```

Server will start at `http://localhost:8000`

### API Documentation
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Docker Installation (Optional)

```bash
# Build Docker image
docker build -t 3d-character-agent .

# Run container
docker run -d -p 8000:8000 \
  -v output:/app/output \
  3d-character-agent
```

## Troubleshooting

### Blender Not Found
```bash
# Check installation
which blender

# Update path in .env
BLENDER_PATH=/path/to/blender
```

### GPU Rendering Not Working
```bash
# Check GPU support
blender --debug-gpu

# Install NVIDIA CUDA Toolkit
# https://developer.nvidia.com/cuda-downloads
```

### Out of Memory Errors
```env
# Reduce render samples
RENDER_SAMPLES=64

# Reduce resolution
RENDER_RESOLUTION=1280x720
```

### Port Already in Use
```bash
# Change API port
API_PORT=8001
python -m src.api.server
```

## Next Steps

1. Review [API Guide](api_guide.md)
2. Check [Examples](examples.md)
3. Explore [Configuration](../README.md#configuration)
