"""
Local data management service for SQLite database and file operations.
"""

import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, Optional, List
import sqlite3
from sqlalchemy.orm import Session
from sqlalchemy import text

from ..config.database import get_local_data_dir, get_db, engine
from ..models.player_context import PlayerContext
from ..models.scenario import Scenario
from ..models.evaluation import Evaluation

class LocalDataService:
    """Service for managing local data storage and backups."""
    
    def __init__(self):
        self.data_dir = get_local_data_dir()
        self.db_path = self.data_dir / "player_data.db"
        
    def get_data_directory(self) -> Path:
        """Get the local data directory path."""
        return self.data_dir
    
    def get_database_path(self) -> Path:
        """Get the SQLite database file path."""
        return self.db_path
    
    def get_database_size(self) -> int:
        """Get the size of the database file in bytes."""
        try:
            return self.db_path.stat().st_size
        except FileNotFoundError:
            return 0
    
    def database_exists(self) -> bool:
        """Check if the database file exists."""
        return self.db_path.exists()
    
    def initialize_database(self) -> None:
        """Initialize the database with tables."""
        try:
            # Import all models to ensure they're registered
            from ..models import scenario, evaluation, player_context
            
            # Create all tables
            from ..config.database import Base
            Base.metadata.create_all(bind=engine)
            
            print(f"✅ Database initialized at: {self.db_path}")
            
        except Exception as e:
            print(f"❌ Error initializing database: {e}")
            raise
    
    def backup_database(self, backup_name: Optional[str] = None) -> Path:
        """Create a backup of the database."""
        if not backup_name:
            backup_name = f"backup_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}.db"
        
        backup_path = self.data_dir / "backups" / backup_name
        
        try:
            shutil.copy2(self.db_path, backup_path)
            print(f"✅ Database backed up to: {backup_path}")
            return backup_path
        except Exception as e:
            print(f"❌ Error backing up database: {e}")
            raise
    
    def restore_database(self, backup_path: Path) -> None:
        """Restore database from backup."""
        try:
            if not backup_path.exists():
                raise FileNotFoundError(f"Backup file not found: {backup_path}")
            
            # Create a backup of current database before restore
            self.backup_database(f"pre_restore_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}.db")
            
            # Restore from backup
            shutil.copy2(backup_path, self.db_path)
            print(f"✅ Database restored from: {backup_path}")
            
        except Exception as e:
            print(f"❌ Error restoring database: {e}")
            raise
    
    def export_player_data(self, player_id: str, db: Session) -> Dict[str, Any]:
        """Export all player data to a dictionary."""
        try:
            # Get player context
            player_context = db.query(PlayerContext).filter(PlayerContext.player_id == player_id).first()
            
            # Get all evaluations
            evaluations = db.query(Evaluation).filter(Evaluation.player_id == player_id).all()
            
            # Get all scenarios the player has encountered
            scenario_ids = [eval.scenario_id for eval in evaluations]
            scenarios = db.query(Scenario).filter(Scenario.scenario_id.in_(scenario_ids)).all()
            
            # Export data
            export_data = {
                "export_info": {
                    "player_id": player_id,
                    "export_date": datetime.now(timezone.utc).isoformat(),
                    "version": "1.0.0"
                },
                "player_context": {
                    "player_id": player_context.player_id,
                    "skill_level": player_context.skill_level,
                    "total_scenarios": player_context.total_scenarios,
                    "correct_decisions": player_context.correct_decisions,
                    "total_sessions": player_context.total_sessions,
                    "total_session_time": player_context.total_session_time,
                    "weaknesses": player_context.weaknesses,
                    "strength_areas": player_context.strength_areas,
                    "focus_areas": player_context.focus_areas,
                    "accuracy_trend": player_context.accuracy_trend,
                    "ev_trend": player_context.ev_trend,
                    "improvement_rate": player_context.improvement_rate,
                    "preferred_difficulty": player_context.preferred_difficulty,
                    "created_at": player_context.created_at.isoformat(),
                    "updated_at": player_context.updated_at.isoformat()
                } if player_context else None,
                "evaluations": [
                    {
                        "evaluation_id": eval.evaluation_id,
                        "scenario_id": eval.scenario_id,
                        "player_action": eval.player_action,
                        "player_amount": eval.player_amount,
                        "time_taken": eval.time_taken,
                        "correct": eval.correct,
                        "optimal_action": eval.optimal_action,
                        "ev_analysis": eval.ev_analysis,
                        "mistake_analysis": eval.mistake_analysis,
                        "coaching_feedback": eval.coaching_feedback,
                        "performance_impact": eval.performance_impact,
                        "key_concepts": eval.key_concepts,
                        "difficulty_assessment": eval.difficulty_assessment,
                        "created_at": eval.created_at.isoformat()
                    } for eval in evaluations
                ],
                "scenarios": [
                    {
                        "scenario_id": scenario.scenario_id,
                        "tournament_stage": scenario.tournament_stage,
                        "hero_position": scenario.hero_position,
                        "hero_stack": scenario.hero_stack,
                        "hero_cards": scenario.hero_cards,
                        "difficulty_level": scenario.difficulty_level,
                        "created_at": scenario.created_at.isoformat()
                    } for scenario in scenarios
                ]
            }
            
            return export_data
            
        except Exception as e:
            print(f"❌ Error exporting player data: {e}")
            raise
    
    def export_player_data_to_file(self, player_id: str, db: Session, filename: Optional[str] = None) -> Path:
        """Export player data to JSON file."""
        if not filename:
            filename = f"player_{player_id}_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}.json"
        
        export_path = self.data_dir / "exports" / filename
        
        try:
            data = self.export_player_data(player_id, db)
            
            with open(export_path, 'w') as f:
                json.dump(data, f, indent=2)
            
            print(f"✅ Player data exported to: {export_path}")
            return export_path
            
        except Exception as e:
            print(f"❌ Error exporting player data to file: {e}")
            raise
    
    def import_player_data_from_file(self, import_path: Path, db: Session) -> str:
        """Import player data from JSON file."""
        try:
            with open(import_path, 'r') as f:
                data = json.load(f)
            
            player_id = data["export_info"]["player_id"]
            
            # Import player context
            if data["player_context"]:
                context_data = data["player_context"]
                
                # Check if player already exists
                existing_player = db.query(PlayerContext).filter(PlayerContext.player_id == player_id).first()
                
                if existing_player:
                    # Update existing player
                    for key, value in context_data.items():
                        if key not in ["created_at", "updated_at"]:
                            setattr(existing_player, key, value)
                    existing_player.updated_at = datetime.now(timezone.utc)
                else:
                    # Create new player
                    new_player = PlayerContext(
                        player_id=context_data["player_id"],
                        skill_level=context_data["skill_level"],
                        total_scenarios=context_data["total_scenarios"],
                        correct_decisions=context_data["correct_decisions"],
                        total_sessions=context_data["total_sessions"],
                        total_session_time=context_data["total_session_time"],
                        weaknesses=context_data["weaknesses"],
                        strength_areas=context_data["strength_areas"],
                        focus_areas=context_data["focus_areas"],
                        accuracy_trend=context_data["accuracy_trend"],
                        ev_trend=context_data["ev_trend"],
                        improvement_rate=context_data["improvement_rate"],
                        preferred_difficulty=context_data["preferred_difficulty"]
                    )
                    db.add(new_player)
            
            db.commit()
            print(f"✅ Player data imported for: {player_id}")
            return player_id
            
        except Exception as e:
            print(f"❌ Error importing player data: {e}")
            raise
    
    def get_database_stats(self) -> Dict[str, Any]:
        """Get database statistics."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Get table counts
                stats = {
                    "database_size": self.get_database_size(),
                    "database_path": str(self.db_path),
                    "created": datetime.fromtimestamp(self.db_path.stat().st_ctime, timezone.utc).isoformat(),
                    "modified": datetime.fromtimestamp(self.db_path.stat().st_mtime, timezone.utc).isoformat(),
                    "tables": {}
                }
                
                # Get table names
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                tables = cursor.fetchall()
                
                for table in tables:
                    table_name = table[0]
                    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                    count = cursor.fetchone()[0]
                    stats["tables"][table_name] = count
                
                return stats
                
        except Exception as e:
            print(f"❌ Error getting database stats: {e}")
            return {"error": str(e)}
    
    def cleanup_old_backups(self, keep_days: int = 30) -> List[Path]:
        """Remove backup files older than specified days."""
        backup_dir = self.data_dir / "backups"
        cutoff_date = datetime.now(timezone.utc).timestamp() - (keep_days * 24 * 60 * 60)
        
        removed_files = []
        
        try:
            for backup_file in backup_dir.glob("*.db"):
                if backup_file.stat().st_mtime < cutoff_date:
                    backup_file.unlink()
                    removed_files.append(backup_file)
            
            if removed_files:
                print(f"✅ Cleaned up {len(removed_files)} old backup files")
            
            return removed_files
            
        except Exception as e:
            print(f"❌ Error cleaning up backups: {e}")
            return []
    
    def get_backup_files(self) -> List[Dict[str, Any]]:
        """Get list of available backup files."""
        backup_dir = self.data_dir / "backups"
        backups = []
        
        try:
            for backup_file in backup_dir.glob("*.db"):
                stat = backup_file.stat()
                backups.append({
                    "filename": backup_file.name,
                    "path": str(backup_file),
                    "size": stat.st_size,
                    "created": datetime.fromtimestamp(stat.st_ctime, timezone.utc).isoformat(),
                    "modified": datetime.fromtimestamp(stat.st_mtime, timezone.utc).isoformat()
                })
            
            # Sort by creation date, newest first
            backups.sort(key=lambda x: x["created"], reverse=True)
            
            return backups
            
        except Exception as e:
            print(f"❌ Error getting backup files: {e}")
            return []

# Create singleton instance
local_data_service = LocalDataService()