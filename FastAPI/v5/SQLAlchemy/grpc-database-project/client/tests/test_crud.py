# ================================
# tests/test_crud.py
import pytest
import structlog
#from client.db_client import DatabaseClient
from client.client.db_client import DatabaseClient

logger = structlog.get_logger()

class TestCRUDOperations:
    def setup_method(self):
        """Setup for each test"""
        self.client = DatabaseClient()
        assert self.client.wait_for_server(), "Server not available"
        
        # Test data
        self.test_table = "rbac_user_info"
        self.test_data = {
            "email": "test@example.com",
            "first_name": "Test",
            "last_name": "User"
        }

    def test_create_record(self):
        """Test creating a record"""
        result = self.client.create_record(self.test_table, self.test_data)
        
        assert result["success"], f"Create failed: {result['message']}"
        assert result["record_id"] > 0, "Record ID should be positive"
        
        # Store for cleanup
        self.record_id = result["record_id"]
        logger.info("Created record", record_id=self.record_id)

    def test_get_record(self):
        """Test getting a record"""
        # First create a record
        create_result = self.client.create_record(self.test_table, self.test_data)
        assert create_result["success"]
        record_id = create_result["record_id"]
        
        # Now get it
        result = self.client.get_record(self.test_table, record_id)
        
        assert result["success"], f"Get failed: {result['message']}"
        assert result["data"]["email"] == self.test_data["email"]
        assert result["data"]["first_name"] == self.test_data["first_name"]
        
        logger.info("Retrieved record", data=result["data"])

    def test_update_record(self):
        """Test updating a record"""
        # Create record
        create_result = self.client.create_record(self.test_table, self.test_data)
        assert create_result["success"]
        record_id = create_result["record_id"]
        
        # Update it
        update_data = {"first_name": "Updated"}
        result = self.client.update_record(self.test_table, record_id, update_data)
        
        assert result["success"], f"Update failed: {result['message']}"
        
        # Verify update
        get_result = self.client.get_record(self.test_table, record_id)
        assert get_result["data"]["first_name"] == "Updated"
        
        logger.info("Updated record", record_id=record_id)

    def test_list_records(self):
        """Test listing records"""
        # Create a few records
        for i in range(3):
            data = self.test_data.copy()
            data["email"] = f"test{i}@example.com"
            self.client.create_record(self.test_table, data)
        
        # List records
        result = self.client.list_records(self.test_table, page=1, page_size=10)
        
        assert result["success"], f"List failed: {result['message']}"
        assert len(result["records"]) >= 3, "Should have at least 3 records"
        assert result["total_count"] >= 3, "Total count should be at least 3"
        
        logger.info("Listed records", count=len(result["records"]))

    def test_delete_record(self):
        """Test deleting a record"""
        # Create record
        create_result = self.client.create_record(self.test_table, self.test_data)
        assert create_result["success"]
        record_id = create_result["record_id"]
        
        # Delete it
        result = self.client.delete_record(self.test_table, record_id)
        
        assert result["success"], f"Delete failed: {result['message']}"
        
        # Verify deletion
        get_result = self.client.get_record(self.test_table, record_id)
        assert not get_result["success"], "Record should not exist after deletion"
        
        logger.info("Deleted record", record_id=record_id)
