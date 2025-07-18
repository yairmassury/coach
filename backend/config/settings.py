"""
Application settings and configuration.
"""

import os
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    """Application settings."""
    
    # Environment
    ENVIRONMENT: str = Field(default="development")
    DEBUG: bool = Field(default=True)
    
    # Database - SQLite Local Storage
    DATABASE_URL: str = Field(default="sqlite:///~/.coach/player_data.db")
    
    # Redis
    REDIS_URL: str = Field(default="redis://localhost:6379/0")
    
    # AI Provider Configuration
    # OpenAI
    OPENAI_API_KEY: Optional[str] = Field(default=None)
    OPENAI_MODEL: str = Field(default="gpt-4")
    OPENAI_BASE_URL: Optional[str] = Field(default=None)
    
    # Anthropic Claude
    ANTHROPIC_API_KEY: Optional[str] = Field(default=None)
    ANTHROPIC_MODEL: str = Field(default="claude-3-5-sonnet-20241022")
    ANTHROPIC_BASE_URL: Optional[str] = Field(default=None)
    
    # Google Gemini
    GOOGLE_API_KEY: Optional[str] = Field(default=None)
    GOOGLE_MODEL: str = Field(default="gemini-1.5-pro")
    GOOGLE_BASE_URL: Optional[str] = Field(default=None)
    
    # OpenRouter
    OPENROUTER_API_KEY: Optional[str] = Field(default=None)
    OPENROUTER_MODEL: str = Field(default="anthropic/claude-3.5-sonnet")
    OPENROUTER_BASE_URL: Optional[str] = Field(default=None)
    
    # XAI Grok
    XAI_API_KEY: Optional[str] = Field(default=None)
    XAI_MODEL: str = Field(default="grok-beta")
    XAI_BASE_URL: Optional[str] = Field(default=None)
    
    # Ollama (local)
    OLLAMA_API_KEY: Optional[str] = Field(default="none")
    OLLAMA_MODEL: str = Field(default="llama3.1:8b")
    OLLAMA_BASE_URL: Optional[str] = Field(default=None)
    
    # AI Settings (applied to all providers)
    AI_TEMPERATURE: float = Field(default=0.7)
    AI_MAX_TOKENS: int = Field(default=2000)
    AI_PROVIDER_TIMEOUT: int = Field(default=30)
    AI_PROVIDER_PRIORITY: str = Field(default="anthropic,openai,google,openrouter,xai,ollama")
    
    # Security
    SECRET_KEY: str = Field(default="your-secret-key-change-this-in-production")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30)
    
    # CORS
    CORS_ORIGINS: str = Field(default="http://localhost:3000")
    
    # Logging
    LOG_LEVEL: str = Field(default="INFO")
    
    # Application
    APP_NAME: str = Field(default="AI Poker Coach")
    APP_VERSION: str = Field(default="1.0.0")
    
    # Server
    HOST: str = Field(default="0.0.0.0")
    PORT: int = Field(default=8000)
    
    # File uploads
    UPLOAD_DIR: str = Field(default="uploads")
    MAX_UPLOAD_SIZE: int = Field(default=10 * 1024 * 1024)  # 10MB
    
    # Session settings
    SESSION_TIMEOUT: int = Field(default=3600)  # 1 hour
    MAX_SCENARIOS_PER_SESSION: int = Field(default=50)
    
    # AI Coach settings
    DEFAULT_DIFFICULTY: str = Field(default="intermediate")
    SCENARIO_CACHE_TTL: int = Field(default=300)  # 5 minutes
    MAX_PLAYER_CONTEXTS: int = Field(default=1000)
    
    # Rate limiting
    RATE_LIMIT_SCENARIOS: int = Field(default=100)  # per hour
    RATE_LIMIT_EVALUATIONS: int = Field(default=200)  # per hour
    
    # Monitoring
    ENABLE_METRICS: bool = Field(default=True)
    SENTRY_DSN: Optional[str] = Field(default=None)
    
    class Config:
        """Pydantic config."""
        env_file = ".env"
        case_sensitive = True

# Create settings instance
_settings = None

def get_settings() -> Settings:
    """Get settings instance (singleton pattern)."""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings

# Environment-specific configurations
def get_database_url() -> str:
    """Get database URL based on environment."""
    settings = get_settings()
    
    if settings.ENVIRONMENT == "test":
        return "sqlite:///./test.db"
    else:
        # Always use local SQLite database
        from pathlib import Path
        data_dir = Path.home() / ".coach"
        data_dir.mkdir(exist_ok=True)
        return f"sqlite:///{data_dir / 'player_data.db'}"

def get_cors_origins() -> list:
    """Get CORS origins as a list."""
    settings = get_settings()
    return settings.CORS_ORIGINS.split(",")

def is_production() -> bool:
    """Check if running in production."""
    settings = get_settings()
    return settings.ENVIRONMENT == "production"

def is_development() -> bool:
    """Check if running in development."""
    settings = get_settings()
    return settings.ENVIRONMENT == "development"

def get_ai_config() -> dict:
    """Get AI configuration."""
    settings = get_settings()
    return {
        "api_key": settings.OPENAI_API_KEY,
        "model": settings.OPENAI_MODEL,
        "temperature": settings.OPENAI_TEMPERATURE,
        "max_tokens": settings.OPENAI_MAX_TOKENS
    }

def validate_ai_config() -> bool:
    """Validate AI configuration."""
    settings = get_settings()
    
    # Check if at least one AI provider is configured
    if not settings.OPENAI_API_KEY and not settings.CLAUDE_API_KEY:
        return False
    
    return True

# Environment variables that should be set
REQUIRED_ENV_VARS = [
    "OPENAI_API_KEY",  # or CLAUDE_API_KEY
    "DATABASE_URL",
    "SECRET_KEY"
]

def check_required_env_vars() -> list:
    """Check which required environment variables are missing."""
    missing_vars = []
    
    for var in REQUIRED_ENV_VARS:
        if var == "OPENAI_API_KEY":
            # Check if any AI provider is configured
            if not os.getenv("OPENAI_API_KEY") and not os.getenv("CLAUDE_API_KEY"):
                missing_vars.append("OPENAI_API_KEY or CLAUDE_API_KEY")
        elif not os.getenv(var):
            missing_vars.append(var)
    
    return missing_vars