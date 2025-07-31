# ================================
# client/db_client.py
import grpc
import json
import time
import structlog
from typing import Dict, Any, List, Optional, Union
from contextlib import contextmanager

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))


# Import generated protobuf files
import database_service_pb2
import database_service_pb2_grpc



from .config import config

logger = structlog.get_logger()

class DatabaseClient:
    """gRPC client for the database service"""
    
    def __init__(self, server_address: Optional[str] = None, timeout: Optional[int] = None):
        self.server_address = server_address or config.server_address
        self.timeout = timeout or config.timeout
        self.max_retries = config.max_retries
        self.retry_delay = config.retry_delay
        
    @contextmanager
    def get_channel(self):
        """Create gRPC channel with proper cleanup"""
        channel = grpc.insecure_channel(self.server_address)
        try:
            yield channel
        finally:
            channel.close()
    
    def _retry_call(self, func, *args, **kwargs):
        """Retry gRPC calls with exponential backoff"""
        for attempt in range(self.max_retries):
            try:
                return func(*args, **kwargs)
            except grpc.RpcError as e:
                if attempt == self.max_retries - 1:
                    logger.error("gRPC call failed after retries", 
                               error=e.details(), 
                               code=e.code().name,
                               attempts=attempt + 1)
                    raise
                
                logger.warning("gRPC call failed, retrying", 
                             error=e.details(), 
                             attempt=attempt + 1,
                             retry_in=self.retry_delay * (2 ** attempt))
                time.sleep(self.retry_delay * (2 ** attempt))
            except Exception as e:
                logger.error("Unexpected error in gRPC call", error=str(e))
                raise

    # ================================
    # CRUD Operations
    # ================================
    
    def create_record(self, table_name: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new record"""
        try:
            with self.get_channel() as channel:
                stub = database_service_pb2_grpc.DatabaseServiceStub(channel)
                request = database_service_pb2.CreateRecordRequest(
                    table_name=table_name,
                    data=json.dumps(data)
                )
                
                response = self._retry_call(
                    stub.CreateRecord, 
                    request, 
                    timeout=self.timeout
                )
                
                return {
                    "success": response.success,
                    "message": response.message,
                    "record_id": response.record_id
                }
        except Exception as e:
            logger.error("Failed to create record", table=table_name, error=str(e))
            return {"success": False, "message": f"Failed to create record: {str(e)}"}

    def get_record(self, table_name: str, record_id: int) -> Dict[str, Any]:
        """Get a record by ID"""
        try:
            with self.get_channel() as channel:
                stub = database_service_pb2_grpc.DatabaseServiceStub(channel)
                request = database_service_pb2.GetRecordRequest(
                    table_name=table_name,
                    record_id=record_id
                )
                
                response = self._retry_call(
                    stub.GetRecord, 
                    request, 
                    timeout=self.timeout
                )
                
                result = {
                    "success": response.success,
                    "message": response.message
                }
                
                if response.success and response.data:
                    result["data"] = json.loads(response.data)
                
                return result
        except Exception as e:
            logger.error("Failed to get record", table=table_name, record_id=record_id, error=str(e))
            return {"success": False, "message": f"Failed to get record: {str(e)}"}

    def update_record(self, table_name: str, record_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update a record"""
        try:
            with self.get_channel() as channel:
                stub = database_service_pb2_grpc.DatabaseServiceStub(channel)
                request = database_service_pb2.UpdateRecordRequest(
                    table_name=table_name,
                    record_id=record_id,
                    data=json.dumps(data)
                )
                
                response = self._retry_call(
                    stub.UpdateRecord, 
                    request, 
                    timeout=self.timeout
                )
                
                return {
                    "success": response.success,
                    "message": response.message
                }
        except Exception as e:
            logger.error("Failed to update record", table=table_name, record_id=record_id, error=str(e))
            return {"success": False, "message": f"Failed to update record: {str(e)}"}

    def delete_record(self, table_name: str, record_id: int) -> Dict[str, Any]:
        """Delete a record"""
        try:
            with self.get_channel() as channel:
                stub = database_service_pb2_grpc.DatabaseServiceStub(channel)
                request = database_service_pb2.DeleteRecordRequest(
                    table_name=table_name,
                    record_id=record_id
                )
                
                response = self._retry_call(
                    stub.DeleteRecord, 
                    request, 
                    timeout=self.timeout
                )
                
                return {
                    "success": response.success,
                    "message": response.message
                }
        except Exception as e:
            logger.error("Failed to delete record", table=table_name, record_id=record_id, error=str(e))
            return {"success": False, "message": f"Failed to delete record: {str(e)}"}

    def list_records(self, table_name: str, page: int = 1, page_size: int = 50, filter_conditions: Optional[str] = None) -> Dict[str, Any]:
        """List records with pagination"""
        try:
            with self.get_channel() as channel:
                stub = database_service_pb2_grpc.DatabaseServiceStub(channel)
                request = database_service_pb2.ListRecordsRequest(
                    table_name=table_name,
                    page=page,
                    page_size=page_size,
                    filter=filter_conditions or ""
                )
                
                response = self._retry_call(
                    stub.ListRecords, 
                    request, 
                    timeout=self.timeout
                )
                
                result = {
                    "success": response.success,
                    "message": response.message,
                    "total_count": response.total_count
                }
                
                if response.success:
                    result["records"] = [json.loads(record) for record in response.records]
                
                return result
        except Exception as e:
            logger.error("Failed to list records", table=table_name, error=str(e))
            return {"success": False, "message": f"Failed to list records: {str(e)}"}

    # ================================
    # Migration Operations
    # ================================
    
    def run_migration(self, direction: str = "upgrade", target_revision: Optional[str] = None) -> Dict[str, Any]:
        """Run database migration"""
        try:
            with self.get_channel() as channel:
                stub = database_service_pb2_grpc.DatabaseServiceStub(channel)
                request = database_service_pb2.MigrationRequest(
                    migration_direction=direction,
                    target_revision=target_revision or ""
                )
                
                response = self._retry_call(
                    stub.RunMigration, 
                    request, 
                    timeout=60  # Migrations might take longer
                )
                
                return {
                    "success": response.success,
                    "message": response.message,
                    "current_revision": response.current_revision
                }
        except Exception as e:
            logger.error("Failed to run migration", direction=direction, error=str(e))
            return {"success": False, "message": f"Failed to run migration: {str(e)}"}

    def get_migration_status(self) -> Dict[str, Any]:
        """Get migration status"""
        try:
            with self.get_channel() as channel:
                stub = database_service_pb2_grpc.DatabaseServiceStub(channel)
                request = database_service_pb2.MigrationStatusRequest()
                
                response = self._retry_call(
                    stub.GetMigrationStatus, 
                    request, 
                    timeout=self.timeout
                )
                
                return {
                    "success": response.success,
                    "current_revision": response.current_revision,
                    "pending_migrations": list(response.pending_migrations)
                }
        except Exception as e:
            logger.error("Failed to get migration status", error=str(e))
            return {"success": False, "message": f"Failed to get migration status: {str(e)}"}

    # ================================
    # Schema Operations
    # ================================
    
    def create_table(self, table_name: str, table_schema: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Create a table"""
        try:
            with self.get_channel() as channel:
                stub = database_service_pb2_grpc.DatabaseServiceStub(channel)
                request = database_service_pb2.CreateTableRequest(
                    table_name=table_name,
                    table_schema=json.dumps(table_schema) if table_schema else ""
                )
                
                response = self._retry_call(
                    stub.CreateTable, 
                    request, 
                    timeout=self.timeout
                )
                
                return {
                    "success": response.success,
                    "message": response.message
                }
        except Exception as e:
            logger.error("Failed to create table", table=table_name, error=str(e))
            return {"success": False, "message": f"Failed to create table: {str(e)}"}

    def add_column(self, table_name: str, column_name: str, column_type: str, 
                   nullable: bool = True, default_value: Optional[str] = None) -> Dict[str, Any]:
        """Add a column to a table"""
        try:
            with self.get_channel() as channel:
                stub = database_service_pb2_grpc.DatabaseServiceStub(channel)
                request = database_service_pb2.AddColumnRequest(
                    table_name=table_name,
                    column_name=column_name,
                    column_type=column_type,
                    nullable=nullable,
                    default_value=default_value or ""
                )
                
                response = self._retry_call(
                    stub.AddColumn, 
                    request, 
                    timeout=self.timeout
                )
                
                return {
                    "success": response.success,
                    "message": response.message
                }
        except Exception as e:
            logger.error("Failed to add column", table=table_name, column=column_name, error=str(e))
            return {"success": False, "message": f"Failed to add column: {str(e)}"}

    def drop_column(self, table_name: str, column_name: str) -> Dict[str, Any]:
        """Drop a column from a table"""
        try:
            with self.get_channel() as channel:
                stub = database_service_pb2_grpc.DatabaseServiceStub(channel)
                request = database_service_pb2.DropColumnRequest(
                    table_name=table_name,
                    column_name=column_name
                )
                
                response = self._retry_call(
                    stub.DropColumn, 
                    request, 
                    timeout=self.timeout
                )
                
                return {
                    "success": response.success,
                    "message": response.message
                }
        except Exception as e:
            logger.error("Failed to drop column", table=table_name, column=column_name, error=str(e))
            return {"success": False, "message": f"Failed to drop column: {str(e)}"}

    # ================================
    # Health Check
    # ================================
    
    def health_check(self) -> Dict[str, Any]:
        """Perform health check"""
        try:
            with self.get_channel() as channel:
                stub = database_service_pb2_grpc.DatabaseServiceStub(channel)
                request = database_service_pb2.HealthCheckRequest()
                
                response = self._retry_call(
                    stub.HealthCheck, 
                    request, 
                    timeout=5  # Shorter timeout for health checks
                )
                
                return {
                    "healthy": response.healthy,
                    "message": response.message,
                    "version": response.version
                }
        except Exception as e:
            logger.error("Health check failed", error=str(e))
            return {"healthy": False, "message": f"Health check failed: {str(e)}"}

    # ================================
    # Convenience Methods
    # ================================
    
    def wait_for_server(self, max_wait_time: int = 60) -> bool:
        """Wait for server to be ready"""
        start_time = time.time()
        while time.time() - start_time < max_wait_time:
            try:
                result = self.health_check()
                if result.get("healthy"):
                    logger.info("Server is ready", server=self.server_address)
                    return True
            except Exception:
                pass
            
            logger.info("Waiting for server to be ready", server=self.server_address)
            time.sleep(2)
        
        logger.error("Server not ready after timeout", timeout=max_wait_time)
        return False
 
