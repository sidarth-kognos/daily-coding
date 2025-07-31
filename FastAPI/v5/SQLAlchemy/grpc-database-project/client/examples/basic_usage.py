# ================================
# examples/basic_usage.py
"""
Basic usage examples for the database client
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import structlog
#from client.db_client import DatabaseClient
#from db_client import DatabaseClient
#from client.db_client import DatabaseClient
from client.client.db_client import DatabaseClient


# Configure logging
structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.add_log_level,
        structlog.processors.JSONRenderer()
    ],
    logger_factory=structlog.PrintLoggerFactory(),
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()

def main():
    # Initialize client
    client = DatabaseClient()
    
    # Wait for server to be ready
    if not client.wait_for_server():
        logger.error("Server not available")
        return
    
    # Health check
    health = client.health_check()
    logger.info("Health check", result=health)
    
    # Create a user record
    user_data = {
        "email": "john.doe@example.com",
        "first_name": "John",
        "last_name": "Doe"
    }
    
    create_result = client.create_record("rbac_user_info", user_data)
    logger.info("Create result", result=create_result)
    
    if create_result["success"]:
        record_id = create_result["record_id"]
        
        # Get the record
        get_result = client.get_record("rbac_user_info", record_id)
        logger.info("Get result", result=get_result)
        
        # Update the record
        update_data = {"first_name": "Johnny"}
        update_result = client.update_record("rbac_user_info", record_id, update_data)
        logger.info("Update result", result=update_result)
        
        # List records
        list_result = client.list_records("rbac_user_info", page=1, page_size=5)
        logger.info("List result", count=len(list_result.get("records", [])))
        
        # Delete the record
        delete_result = client.delete_record("rbac_user_info", record_id)
        logger.info("Delete result", result=delete_result)

if __name__ == "__main__":
    main()
 
