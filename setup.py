#!/usr/bin/env python3
"""
Setup script for AI Poker Coach - Local SQLite Version
"""

import os
import sys
from pathlib import Path

def create_local_directories():
    """Create local data directories."""
    home_dir = Path.home()
    data_dir = home_dir / ".coach"
    
    # Create main directory
    data_dir.mkdir(exist_ok=True)
    print(f"✅ Created data directory: {data_dir}")
    
    # Create subdirectories
    subdirs = ["backups", "exports", "logs"]
    for subdir in subdirs:
        (data_dir / subdir).mkdir(exist_ok=True)
        print(f"✅ Created subdirectory: {data_dir / subdir}")
    
    return data_dir

def initialize_database():
    """Initialize the SQLite database."""
    try:
        # Add the backend directory to Python path
        backend_dir = Path(__file__).parent / "backend"
        sys.path.insert(0, str(backend_dir))
        
        from services.local_data_service import local_data_service
        local_data_service.initialize_database()
        print("✅ Database initialized successfully")
        
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        return False
    
    return True

def check_requirements():
    """Check if Python requirements are met."""
    try:
        import fastapi
        import sqlalchemy
        import openai
        print("✅ All required packages are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing required package: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def main():
    """Main setup function."""
    print("🚀 Setting up AI Poker Coach - Local Version")
    print("=" * 50)
    
    # Check requirements
    if not check_requirements():
        return False
    
    # Create directories
    data_dir = create_local_directories()
    
    # Initialize database
    if not initialize_database():
        return False
    
    # Check for OpenAI API key
    openai_key = os.getenv("OPENAI_API_KEY")
    if not openai_key:
        print("⚠️  Warning: OPENAI_API_KEY not set")
        print("Please set your OpenAI API key in the .env file")
    else:
        print("✅ OpenAI API key configured")
    
    print("\n" + "=" * 50)
    print("🎯 Setup complete!")
    print(f"📁 Data directory: {data_dir}")
    print(f"🗄️  Database: {data_dir / 'player_data.db'}")
    print("\n📋 Next steps:")
    print("1. Make sure your .env file has your OpenAI API key")
    print("2. Start the backend: uvicorn main:app --reload")
    print("3. Start the frontend: cd frontend && npm start")
    print("4. Open http://localhost:3000 in your browser")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)