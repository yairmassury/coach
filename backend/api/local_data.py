"""
Local data management API endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from pathlib import Path
import json

from ..services.local_data_service import local_data_service
from ..config.database import get_db

router = APIRouter(prefix="/local", tags=["local-data"])

@router.get("/info")
async def get_local_data_info():
    """Get information about local data storage."""
    
    try:
        data_dir = local_data_service.get_data_directory()
        db_path = local_data_service.get_database_path()
        
        return {
            "data_directory": str(data_dir),
            "database_path": str(db_path),
            "database_exists": local_data_service.database_exists(),
            "database_size": local_data_service.get_database_size(),
            "database_size_mb": round(local_data_service.get_database_size() / (1024 * 1024), 2)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/initialize")
async def initialize_database():
    """Initialize the local database."""
    
    try:
        local_data_service.initialize_database()
        return {"message": "Database initialized successfully"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stats")
async def get_database_stats():
    """Get database statistics."""
    
    try:
        stats = local_data_service.get_database_stats()
        return stats
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/backup")
async def create_backup(backup_name: Optional[str] = None):
    """Create a backup of the database."""
    
    try:
        backup_path = local_data_service.backup_database(backup_name)
        return {
            "message": "Backup created successfully",
            "backup_path": str(backup_path),
            "backup_name": backup_path.name
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/backups")
async def list_backups():
    """List available backup files."""
    
    try:
        backups = local_data_service.get_backup_files()
        return {"backups": backups}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/restore")
async def restore_from_backup(backup_filename: str):
    """Restore database from backup."""
    
    try:
        backup_path = local_data_service.get_data_directory() / "backups" / backup_filename
        
        if not backup_path.exists():
            raise HTTPException(status_code=404, detail="Backup file not found")
        
        local_data_service.restore_database(backup_path)
        return {"message": f"Database restored from {backup_filename}"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/export/{player_id}")
async def export_player_data(player_id: str, db: Session = Depends(get_db)):
    """Export player data to JSON file."""
    
    try:
        export_path = local_data_service.export_player_data_to_file(player_id, db)
        return {
            "message": "Player data exported successfully",
            "export_path": str(export_path),
            "filename": export_path.name
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/export/{player_id}/data")
async def get_player_export_data(player_id: str, db: Session = Depends(get_db)):
    """Get player data as JSON (for download)."""
    
    try:
        data = local_data_service.export_player_data(player_id, db)
        return data
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/import")
async def import_player_data(import_filename: str, db: Session = Depends(get_db)):
    """Import player data from JSON file."""
    
    try:
        import_path = local_data_service.get_data_directory() / "exports" / import_filename
        
        if not import_path.exists():
            raise HTTPException(status_code=404, detail="Import file not found")
        
        player_id = local_data_service.import_player_data_from_file(import_path, db)
        return {
            "message": "Player data imported successfully",
            "player_id": player_id
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/cleanup")
async def cleanup_old_backups(keep_days: int = 30):
    """Clean up old backup files."""
    
    try:
        removed_files = local_data_service.cleanup_old_backups(keep_days)
        return {
            "message": f"Cleaned up {len(removed_files)} old backup files",
            "removed_files": [str(f) for f in removed_files],
            "keep_days": keep_days
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/exports")
async def list_export_files():
    """List available export files."""
    
    try:
        exports_dir = local_data_service.get_data_directory() / "exports"
        export_files = []
        
        for export_file in exports_dir.glob("*.json"):
            stat = export_file.stat()
            export_files.append({
                "filename": export_file.name,
                "path": str(export_file),
                "size": stat.st_size,
                "created": stat.st_ctime,
                "modified": stat.st_mtime
            })
        
        # Sort by creation date, newest first
        export_files.sort(key=lambda x: x["created"], reverse=True)
        
        return {"exports": export_files}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/directory")
async def open_data_directory():
    """Get the path to the data directory (for opening in file manager)."""
    
    try:
        data_dir = local_data_service.get_data_directory()
        return {
            "data_directory": str(data_dir),
            "exists": data_dir.exists(),
            "message": f"Data directory: {data_dir}"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def local_data_health_check():
    """Health check for local data system."""
    
    try:
        data_dir = local_data_service.get_data_directory()
        db_exists = local_data_service.database_exists()
        
        health_status = {
            "status": "healthy" if db_exists else "needs_initialization",
            "data_directory_exists": data_dir.exists(),
            "database_exists": db_exists,
            "database_size": local_data_service.get_database_size(),
            "writable": data_dir.exists() and data_dir.is_dir()
        }
        
        return health_status
        
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        }