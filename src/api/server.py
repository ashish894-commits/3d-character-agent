"""FastAPI application and server setup"""

import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.config import Settings
from .routes import router

# Configure logging
logging.basicConfig(
    level=Settings.LOG_LEVEL,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(Settings.LOG_FILE),
        logging.StreamHandler(),
    ]
)

logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="3D Character Agent API",
    description="AI-powered 3D character creation and animation agent",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(router)


@app.on_event("startup")
async def startup_event():
    """Initialize on startup"""
    logger.info("3D Character Agent API starting up...")
    logger.info(f"Blender Path: {Settings.BLENDER_PATH}")
    logger.info(f"Output Directory: {Settings.OUTPUT_DIR}")
    logger.info(f"Render Engine: {Settings.RENDER_ENGINE}")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("3D Character Agent API shutting down...")


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )


if __name__ == "__main__":
    import uvicorn
    
    logger.info(f"Starting server on {Settings.API_HOST}:{Settings.API_PORT}")
    uvicorn.run(
        app,
        host=Settings.API_HOST,
        port=Settings.API_PORT,
        workers=Settings.API_WORKERS,
    )
