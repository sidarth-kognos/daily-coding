# ================================
# examples/migration_example.py
"""
Migration management examples
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import structlog
#from client.db_client import DatabaseClient
from client.client.db_client import DatabaseClient

logger = structlog.get_logger()

def main():
    client = DatabaseClient()
    
    if not client.wait_for_server():
        logger.error("Server not available")
        return
    
    # Get current migration status
    status = client.get_migration_status()
    logger.info("Migration status", status=status)
    
    # Run migration upgrade
    upgrade_result = client.run_migration("upgrade")
    logger.info("Migration upgrade", result=upgrade_result)
    
    # Get status after migration
    status_after = client.get_migration_status()
    logger.info("Migration status after upgrade", status=status_after)

if __name__ == "__main__":
    main()
 
