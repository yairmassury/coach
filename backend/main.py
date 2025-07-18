"""
Main FastAPI application for AI Poker Coach.
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import uvicorn
import os
from datetime import datetime

# Import routers
from .api.games import router as games_router
from .api.ai_coach import router as ai_coach_router
from .api.local_data import router as local_data_router

# Import database
from .config.database import create_tables, get_db

# Import settings
from .config.settings import get_settings

settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    print("=� Starting AI Poker Coach API...")
    
    # Create database tables
    try:
        create_tables()
        print(" Database tables created successfully")
    except Exception as e:
        print(f"L Error creating database tables: {e}")
    
    # Verify AI service configuration
    try:
        if not settings.OPENAI_API_KEY:
            print("�  Warning: OPENAI_API_KEY not configured")
        else:
            print(" OpenAI API key configured")
    except Exception as e:
        print(f"L Error checking AI configuration: {e}")
    
    print("<� AI Poker Coach API ready!")
    
    yield
    
    # Shutdown
    print("=� Shutting down AI Poker Coach API...")

# Create FastAPI app
app = FastAPI(
    title="AI Poker Coach",
    description="AI-powered MTT poker coaching application",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(games_router, prefix="/api")
app.include_router(ai_coach_router, prefix="/api")
app.include_router(local_data_router, prefix="/api")

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "ai-poker-coach",
        "timestamp": datetime.utcnow(),
        "version": "1.0.0"
    }

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "AI Poker Coach API",
        "version": "1.0.0",
        "description": "AI-powered MTT poker coaching application",
        "endpoints": {
            "health": "/health",
            "docs": "/docs",
            "redoc": "/redoc",
            "games": "/api/games",
            "ai_coach": "/api/ai",
            "local_data": "/api/local"
        }
    }

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler."""
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": str(exc),
            "timestamp": datetime.utcnow().isoformat()
        }
    )

# HTTP exception handler
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """HTTP exception handler."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code,
            "timestamp": datetime.utcnow().isoformat()
        }
    )

# Development server
if __name__ == "__main__":
    # Get port from environment or use default
    port = int(os.environ.get("PORT", 8000))
    
    # Run the server
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=True,
        log_level="info"
    )