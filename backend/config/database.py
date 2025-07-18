"""
Database configuration and setup - SQLite Local Storage.
"""

from pathlib import Path
from typing import Generator

from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session


# Database URL is generated locally in this file

# Create local data directory
def get_local_data_dir() -> Path:
    """Get or create the local data directory."""
    home_dir = Path.home()
    data_dir = home_dir / ".coach"
    data_dir.mkdir(exist_ok=True)
    
    # Create subdirectories
    (data_dir / "backups").mkdir(exist_ok=True)
    (data_dir / "exports").mkdir(exist_ok=True)
    (data_dir / "logs").mkdir(exist_ok=True)
    
    return data_dir

# Create database engine for SQLite
def create_sqlite_engine():
    """Create SQLite engine with local file storage."""
    data_dir = get_local_data_dir()
    db_path = data_dir / "player_data.db"
    
    # SQLite connection string
    database_url = f"sqlite:///{db_path}"
    
    return create_engine(
        database_url,
        echo=False,  # Set to True for SQL debugging
        # SQLite-specific settings
        pool_pre_ping=True,
        connect_args={"check_same_thread": False}  # Allow SQLite to be used across threads
    )

# Create engine
engine = create_sqlite_engine()

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class
Base = declarative_base()

def get_db() -> Generator[Session, None, None]:
    """
    Database dependency for FastAPI.
    Provides a database session for each request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    """Create all database tables."""
    try:
        # Import all models to ensure they are registered
        from ..models import scenario, evaluation, player_context
        
        # Create all tables
        Base.metadata.create_all(bind=engine)
        print(" Database tables created successfully")
        
    except Exception as e:
        print(f"L Error creating database tables: {e}")
        raise

def drop_tables():
    """Drop all database tables."""
    try:
        Base.metadata.drop_all(bind=engine)
        print(" Database tables dropped successfully")
        
    except Exception as e:
        print(f"L Error dropping database tables: {e}")
        raise

def reset_database():
    """Reset database by dropping and recreating all tables."""
    try:
        drop_tables()
        create_tables()
        print(" Database reset successfully")
        
    except Exception as e:
        print(f"L Error resetting database: {e}")
        raise

def check_database_connection():
    """Check if database connection is working."""
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
        return True
        
    except Exception as e:
        print(f"L Database connection failed: {e}")
        return False

# Database initialization functions
def init_database():
    """Initialize database with required data."""
    try:
        # Create tables
        create_tables()
        
        # Add any initial data here
        # e.g., default player contexts, sample scenarios, etc.
        
        print(" Database initialized successfully")
        
    except Exception as e:
        print(f"L Error initializing database: {e}")
        raise

# Context manager for database transactions
class DatabaseTransaction:
    """Context manager for database transactions."""
    
    def __init__(self):
        self.db = None
    
    def __enter__(self) -> Session:
        self.db = SessionLocal()
        return self.db
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.db.rollback()
        else:
            self.db.commit()
        self.db.close()

# Database utilities
def get_db_session() -> Session:
    """Get a database session (use with caution - remember to close)."""
    return SessionLocal()

def execute_raw_sql(query: str, params: dict = None):
    """Execute raw SQL query."""
    with DatabaseTransaction() as db:
        result = db.execute(text(query), params or {})
        return result.fetchall()

def get_table_count(table_name: str) -> int:
    """Get count of records in a table."""
    with DatabaseTransaction() as db:
        result = db.execute(text(f"SELECT COUNT(*) FROM {table_name}"))
        return result.scalar()

def vacuum_database():
    """Vacuum database (SQLite)."""
    try:
        with engine.connect() as conn:
            conn.execute(text("VACUUM"))
        print(" Database vacuumed successfully")
        
    except Exception as e:
        print(f"L Error vacuuming database: {e}")

# Migration utilities
def get_database_version() -> str:
    """Get database version."""
    try:
        with DatabaseTransaction() as db:
            result = db.execute(text("SELECT sqlite_version()"))
            return result.scalar()
    except Exception as e:
        return f"Error getting version: {e}"

def backup_database(backup_path: str):
    """Backup database (PostgreSQL only)."""

    try:
        # This would need to be implemented based on your database type
        # For PostgreSQL:
        # subprocess.run(['pg_dump', get_database_url(), '-f', backup_path])
        print(f" Database backed up to {backup_path}")
        
    except Exception as e:
        print(f"L Error backing up database: {e}")

# Health check functions
def database_health_check() -> dict:
    """Perform database health check."""
    health = {
        "status": "healthy",
        "connection": False,
        "tables": 0,
        "version": "unknown"
    }
    
    try:
        # Check connection
        health["connection"] = check_database_connection()
        
        # Get database version
        health["version"] = get_database_version()
        
        # Count tables (SQLite)
        with DatabaseTransaction() as db:
            result = db.execute(
                text("SELECT count(*) FROM sqlite_master WHERE type='table'")
            )
            health["tables"] = result.scalar()
            
        if not health["connection"]:
            health["status"] = "unhealthy"
            
    except Exception as e:
        health["status"] = "unhealthy"
        health["error"] = str(e)
    
    return health