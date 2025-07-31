 # ================================
# main.py
import structlog
import sys
import os

# Configure logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

from app.grpc_server import serve
from app.database import engine, Base
from app.config import settings

logger = structlog.get_logger()

def create_tables():
    """Create all tables using SQLAlchemy metadata"""
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully using SQLAlchemy")
    except Exception as e:
        logger.error("Failed to create tables", error=str(e))
        sys.exit(1)

def run_initial_migration():
    """Run initial migration using Alembic (preferred for production)"""
    from alembic.config import Config
    from alembic import command

    try:
        print("⚙️  Running Alembic migration...")
        alembic_cfg = Config("alembic.ini")
        command.upgrade(alembic_cfg, "head")
        print("✅ Alembic migration done.")
        logger.info("Database migration completed successfully")
    except Exception as e:
        logger.error("Failed to run migration", error=str(e))



def initialize_database():
    """Initialize database - choose between direct table creation or migration"""
    init_method = os.getenv("DB_INIT_METHOD", "migration")  # "migration" or "create_tables"
    
    if init_method == "migration":
        logger.info("Initializing database using Alembic migrations")
        run_initial_migration()
    else:
        logger.info("Initializing database using direct table creation")
        create_tables()
"""
if __name__ == "__main__":
    logger.info("Starting Database gRPC Server", port=settings.grpc_port)
    
    # Initialize database on startup
    initialize_database()
    
    # Start gRPC server
    serve()
"""
if __name__ == "__main__":
    logger.info("Starting Database gRPC Server", port=settings.grpc_port)

    print("🔍 About to initialize database...")
    initialize_database()
    print("✅ Database initialized.")
    print("🚀 Launching gRPC server...")
    logger.info("🚀 Launching gRPC server...")
    serve()


