# ================================
# examples/bulk_operations.py
"""
Bulk operations and performance testing
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import time
import structlog
#from client.db_client import DatabaseClient
from client.client.db_client import DatabaseClient

logger = structlog.get_logger()



def bulk_create_test(client: DatabaseClient, count: int = 100):
    """Test bulk creation of records"""
    table_name = "rbac_user_info"
    
    start_time = time.time()
    created_ids = []
    
    for i in range(count):
        data = {
            "email": f"bulk_user_{i}@example.com",
            "first_name": f"User{i}",
            "last_name": "BulkTest"
        }
        
        result = client.create_record(table_name, data)
        if result["success"]:
            created_ids.append(result["record_id"])
        else:
            logger.error("Failed to create record", index=i, error=result["message"])
    
    end_time = time.time()
    duration = end_time - start_time
    
    logger.info("Bulk create completed", 
               count=len(created_ids),
               duration=duration,
               rate=len(created_ids)/duration)
    
    return created_ids

def bulk_read_test(client: DatabaseClient, record_ids: list):
    """Test bulk reading of records"""
    table_name = "rbac_user_info"
    
    start_time = time.time()
    success_count = 0
    
    for record_id in record_ids:
        result = client.get_record(table_name, record_id)
        if result["success"]:
            success_count += 1
    
    end_time = time.time()
    duration = end_time - start_time
    
    logger.info("Bulk read completed",
               total=len(record_ids),
               success=success_count,
               duration=duration,
               rate=success_count/duration)

def main():
    client = DatabaseClient()
    
    if not client.wait_for_server():
        logger.error("Server not available")
        return
    
    # Bulk create test
    logger.info("Starting bulk create test")
    created_ids = bulk_create_test(client, 50)
    
    # Bulk read test
    logger.info("Starting bulk read test")
    bulk_read_test(client, created_ids)
    
    # Cleanup - bulk delete
    logger.info("Cleaning up test records")
    for record_id in created_ids:
        client.delete_record("rbac_user_info", record_id)

if __name__ == "__main__":
    main()

