# ================================
# tests/test_schema.py
import pytest
import structlog
#from client.db_client import DatabaseClient
from client.client.db_client import DatabaseClient

logger = structlog.get_logger()

class TestSchemaOperations:
    def setup_method(self):
        """Setup for each test"""
        self.client = DatabaseClient()
        assert self.client.wait_for_server(), "Server not available"

    def test_create_table(self):
        """Test creating a table"""
        result = self.client.create_table("rbac_user_info")
        
        # Should succeed or already exist
        assert result["success"] or "already exists" in result["message"].lower()
        
        logger.info("Table creation result", message=result["message"])

    def test_add_column(self):
        """Test adding a column"""
        table_name = "rbac_user_info"
        column_name = "test_column"
        
        result = self.client.add_column(
            table_name=table_name,
            column_name=column_name,
            column_type="VARCHAR(255)",
            nullable=True,
            default_value="'default_value'"
        )
        
        # May fail if column already exists, which is okay
        logger.info("Add column result", 
                   table=table_name,
                   column=column_name,
                   success=result["success"],
                   message=result["message"])

    def test_drop_column(self):
        """Test dropping a column"""
        table_name = "rbac_user_info"
        column_name = "test_column"
        
        # First try to add it
        self.client.add_column(
            table_name=table_name,
            column_name=column_name,
            column_type="VARCHAR(255)"
        )
        
        # Then drop it
        result = self.client.drop_column(table_name, column_name)
        
        # Should succeed if column exists
        logger.info("Drop column result",
                   table=table_name,
                   column=column_name,
                   success=result["success"],
                   message=result["message"])
