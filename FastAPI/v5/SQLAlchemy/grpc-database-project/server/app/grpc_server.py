# ================================
# app/grpc_server.py
import grpc
import json
import structlog
from concurrent import futures
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'proto'))
# Add the parent directory to the path so we can import generated protobuf files
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import generated protobuf files (you'll need to generate these)
# import database_service_pb2

from app.services.db_service import DatabaseService
import database_service_pb2_grpc
import database_service_pb2


from .config import settings

logger = structlog.get_logger()

class DatabaseServicer(database_service_pb2_grpc.DatabaseServiceServicer):
    def __init__(self):
        self.db_service = DatabaseService()

    def CreateRecord(self, request, context):
        """Create a new record"""
        try:
            data = json.loads(request.data)
            result = self.db_service.create_record(request.table_name, data)
            
            return database_service_pb2.CreateRecordResponse(
                success=result["success"],
                message=result["message"],
                record_id=result.get("record_id", 0)
            )
        except Exception as e:
            logger.error("CreateRecord failed", error=str(e))
            return database_service_pb2.CreateRecordResponse(
                success=False,
                message=f"CreateRecord failed: {str(e)}",
                record_id=0
            )


    def GetRecord(self, request, context):
        """Get a record by ID"""
        try:
            result = self.db_service.get_record(request.table_name, request.record_id)
            
            return database_service_pb2.GetRecordResponse(
                success=result["success"],
                message=result["message"],
                data=result.get("data", "")
            )
        except Exception as e:
            logger.error("GetRecord failed", error=str(e))
            return database_service_pb2.GetRecordResponse(
                success=False,
                message=f"GetRecord failed: {str(e)}",
                data=""
            )


    def UpdateRecord(self, request, context):
        """Update a record"""
        try:
            data = json.loads(request.data)
            result = self.db_service.update_record(request.table_name, request.record_id, data)
            
            return database_service_pb2.UpdateRecordResponse(
                success=result["success"],
                message=result["message"]
            )
        except Exception as e:
            logger.error("UpdateRecord failed", error=str(e))
            return database_service_pb2.UpdateRecordResponse(
                success=False,
                message=f"UpdateRecord failed: {str(e)}"
            )


    def DeleteRecord(self, request, context):
        """Delete a record"""
        try:
            result = self.db_service.delete_record(request.table_name, request.record_id)
            
            return database_service_pb2.DeleteRecordResponse(
                success=result["success"],
                message=result["message"]
            )
        except Exception as e:
            logger.error("DeleteRecord failed", error=str(e))
            return database_service_pb2.DeleteRecordResponse(
                success=False,
                message=f"DeleteRecord failed: {str(e)}"
            )


    def ListRecords(self, request, context):
        """List records with pagination"""
        try:
            result = self.db_service.list_records(
                request.table_name, 
                request.page, 
                request.page_size,
                request.filter if request.filter else None
            )
            
            return database_service_pb2.ListRecordsResponse(
                success=result["success"],
                message=result["message"],
                records=result.get("records", []),
                total_count=result.get("total_count", 0)
            )
        except Exception as e:
            logger.error("ListRecords failed", error=str(e))
            return database_service_pb2.ListRecordsResponse(
                success=False,
                message=f"ListRecords failed: {str(e)}",
                records=[],
                total_count=0
            )


    def RunMigration(self, request, context):
        """Run database migration"""
        try:
            result = self.db_service.run_migration(
                request.migration_direction,
                request.target_revision if request.target_revision else None
            )
            
            return database_service_pb2.MigrationResponse(
                success=result["success"],
                message=result["message"],
                current_revision=result.get("current_revision", "")
            )
        except Exception as e:
            logger.error("RunMigration failed", error=str(e))
            return database_service_pb2.MigrationResponse(
                success=False,
                message=f"RunMigration failed: {str(e)}",
                current_revision=""
            )


    def GetMigrationStatus(self, request, context):
        """Get migration status"""
        try:
            result = self.db_service.get_migration_status()
            
            return database_service_pb2.MigrationStatusResponse(
                success=result["success"],
                current_revision=result.get("current_revision", ""),
                pending_migrations=result.get("pending_migrations", [])
            )
        except Exception as e:
            logger.error("GetMigrationStatus failed", error=str(e))
            return database_service_pb2.MigrationStatusResponse(
                success=False,
                current_revision="",
                pending_migrations=[]
            )


    def CreateTable(self, request, context):
        """Create a table"""
        try:
            schema = json.loads(request.table_schema) if request.table_schema else None
            result = self.db_service.create_table(request.table_name, schema)
            
            return database_service_pb2.CreateTableResponse(
                success=result["success"],
                message=result["message"]
            )
        except Exception as e:
            logger.error("CreateTable failed", error=str(e))
            return database_service_pb2.CreateTableResponse(
                success=False,
                message=f"CreateTable failed: {str(e)}"
            )


    def AddColumn(self, request, context):
        """Add column to table"""
        try:
            result = self.db_service.add_column(
                request.table_name,
                request.column_name,
                request.column_type,
                request.nullable,
                request.default_value if request.default_value else None
            )
            
            return database_service_pb2.AddColumnResponse(
                success=result["success"],
                message=result["message"]
            )
        except Exception as e:
            logger.error("AddColumn failed", error=str(e))
            return database_service_pb2.AddColumnResponse(
                success=False,
                message=f"AddColumn failed: {str(e)}"
            )


    def DropColumn(self, request, context):
        """Drop column from table"""
        try:
            result = self.db_service.drop_column(request.table_name, request.column_name)
            
            return database_service_pb2.DropColumnResponse(
                success=result["success"],
                message=result["message"]
            )
        except Exception as e:
            logger.error("DropColumn failed", error=str(e))
            return database_service_pb2.DropColumnResponse(
                success=False,
                message=f"DropColumn failed: {str(e)}"
            )


    def HealthCheck(self, request, context):
        """Health check"""
        logger.info("🔍 Received HealthCheck request")
        try:
            result = self.db_service.health_check()
            
            return database_service_pb2.HealthCheckResponse(
                healthy=result["healthy"],
                message=result["message"],
                version=result["version"]
            )
        except Exception as e:
            logger.error("HealthCheck failed", error=str(e))
            return database_service_pb2.HealthCheckResponse(
                healthy=False,
                message=f"HealthCheck failed: {str(e)}",
                version="1.0.0"
            )

from app.services.db_service import DatabaseService
from proto import database_service_pb2_grpc
from grpc_reflection.v1alpha import reflection
import database_service_pb2

from grpc_reflection.v1alpha import reflection

def serve():
    print("🔥 Inside serve()")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=settings.max_workers))

    # Register your service implementation
    database_service_pb2_grpc.add_DatabaseServiceServicer_to_server(
        DatabaseServicer(), server
    )

    # Enable reflection
    SERVICE_NAMES = (
        database_service_pb2.DESCRIPTOR.services_by_name['DatabaseService'].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(SERVICE_NAMES, server)

    listen_addr = f'[::]:{settings.grpc_port}'
    server.add_insecure_port(listen_addr)

    logger.info("Starting gRPC server", address=listen_addr)
    server.start()

    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        logger.info("Shutting down gRPC server")
        server.stop(0)


 
