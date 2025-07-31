# ================================
# tests/test_migrations.py
import pytest
import structlog
#from client.db_client import DatabaseClient
from client.client.db_client import DatabaseClient

logger = structlog.get_logger()

class TestMigrations:
    def setup_method(self):
        """Setup for each test"""
        self.client = DatabaseClient()
        assert self.client.wait_for_server(), "Server not available"

    def test_migration_status(self):
        """Test getting migration status"""
        result = self.client.get_migration_status()
        
        assert result["success"], f"Migration status failed: {result.get('message', '')}"
        assert "current_revision" in result
        assert "pending_migrations" in result
        
        logger.info("Migration status", 
                   current_revision=result["current_revision"],
                   pending_count=len(result["pending_migrations"]))

    def test_run_migration_upgrade(self):
        """Test running migration upgrade"""
        result = self.client.run_migration("upgrade")
        
        assert result["success"], f"Migration upgrade failed: {result['message']}"
        assert "current_revision" in result
        
        logger.info("Migration upgrade completed", 
                   revision=result["current_revision"])
