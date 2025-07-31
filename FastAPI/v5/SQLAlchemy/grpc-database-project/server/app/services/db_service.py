# ================================
# app/services/db_service.py
import json
import structlog
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import inspect, text
from alembic.config import Config
from alembic import command
from alembic.runtime.migration import MigrationContext
from alembic.script import ScriptDirectory

from ..database import get_db_session, engine, Base
from ..models.tables import *

logger = structlog.get_logger()

class DatabaseService:
    def __init__(self):
        self.table_mapping = {
            'EMR_Cluster_Configuration': EMRClusterConfiguration,
            'emr_job_runs_status': EMRJobRunsStatus,
            'emr_job_settings': EMRJobSettings,
            'iq_metering_data_processed_records': IQMeteringDataProcessedRecords,
            'iq_metering_event_summary_records': IQMeteringEventSummaryRecords,
            'iq_metering_object_records': IQMeteringObjectRecords,
            'job_data_selection': JobDataSelection,
            'osdu_instance_settings': OSDUInstanceSettings,
            'osdu_usage_statistics': OSDUUsageStatistics,
            'osdu_user_token': OSDUUserToken,
            'project_settings': ProjectSettings,
            'rbac_module_info': RBACModuleInfo,
            'rbac_role_category': RBACRoleCategory,
            'rbac_role_info': RBACRoleInfo,
            'rbac_role_module_permission': RBACRoleModulePermission,
            'rbac_role_settings': RBACRoleSettings,
            'rbac_user_info': RBACUserInfo,
            'rbac_user_role_assignment': RBACUserRoleAssignment,
            'segy_scan_data': SegyScanData,
            'segy_to_vds_info': SegyToVdsInfo,
            'segy_to_vds_status': SegyToVdsStatus,
            'settings_app_registration': SettingsAppRegistration,
            'settings_de_tree': SettingsDeTree,
            'settings_user_logging': SettingsUserLogging,
            'user_settings': UserSettings,
            'user':user,
        }

    def get_model_class(self, table_name: str):
        return self.table_mapping.get(table_name)

    def create_record(self, table_name: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new record in the specified table"""
        try:
            model_class = self.get_model_class(table_name)
            if not model_class:
                return {"success": False, "message": f"Table {table_name} not found"}

            with get_db_session() as session:
                # Create new instance
                record = model_class(**data)
                session.add(record)
                session.flush()  # Get the ID before commit
                
                record_id = record.id
                session.commit()
                
                logger.info("Record created", table=table_name, record_id=record_id)
                return {
                    "success": True, 
                    "message": "Record created successfully",
                    "record_id": record_id
                }
        except Exception as e:
            logger.error("Failed to create record", table=table_name, error=str(e))
            return {"success": False, "message": f"Failed to create record: {str(e)}"}

    def get_record(self, table_name: str, record_id: int) -> Dict[str, Any]:
        """Get a record by ID from the specified table"""
        try:
            model_class = self.get_model_class(table_name)
            if not model_class:
                return {"success": False, "message": f"Table {table_name} not found"}

            with get_db_session() as session:
                record = session.query(model_class).filter(model_class.id == record_id).first()
                
                if not record:
                    return {"success": False, "message": "Record not found"}
                
                # Convert to dict
                record_dict = {}
                for column in model_class.__table__.columns:
                    value = getattr(record, column.name)
                    if isinstance(value, datetime):
                        value = value.isoformat()
                    record_dict[column.name] = value
                
                return {
                    "success": True,
                    "message": "Record retrieved successfully",
                    "data": json.dumps(record_dict)
                }
        except Exception as e:
            logger.error("Failed to get record", table=table_name, record_id=record_id, error=str(e))
            return {"success": False, "message": f"Failed to get record: {str(e)}"}

    def update_record(self, table_name: str, record_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update a record in the specified table"""
        try:
            model_class = self.get_model_class(table_name)
            if not model_class:
                return {"success": False, "message": f"Table {table_name} not found"}

            with get_db_session() as session:
                record = session.query(model_class).filter(model_class.id == record_id).first()
                
                if not record:
                    return {"success": False, "message": "Record not found"}
                
                # Update fields
                for key, value in data.items():
                    if hasattr(record, key):
                        setattr(record, key, value)
                
                session.commit()
                
                logger.info("Record updated", table=table_name, record_id=record_id)
                return {"success": True, "message": "Record updated successfully"}
        except Exception as e:
            logger.error("Failed to update record", table=table_name, record_id=record_id, error=str(e))
            return {"success": False, "message": f"Failed to update record: {str(e)}"}

    def delete_record(self, table_name: str, record_id: int) -> Dict[str, Any]:
        """Delete a record from the specified table"""
        try:
            model_class = self.get_model_class(table_name)
            if not model_class:
                return {"success": False, "message": f"Table {table_name} not found"}

            with get_db_session() as session:
                record = session.query(model_class).filter(model_class.id == record_id).first()
                
                if not record:
                    return {"success": False, "message": "Record not found"}
                
                session.delete(record)
                session.commit()
                
                logger.info("Record deleted", table=table_name, record_id=record_id)
                return {"success": True, "message": "Record deleted successfully"}
        except Exception as e:
            logger.error("Failed to delete record", table=table_name, record_id=record_id, error=str(e))
            return {"success": False, "message": f"Failed to delete record: {str(e)}"}

    def list_records(self, table_name: str, page: int = 1, page_size: int = 50, filter_conditions: Optional[str] = None) -> Dict[str, Any]:
        """List records from the specified table with pagination"""
        try:
            model_class = self.get_model_class(table_name)
            if not model_class:
                return {"success": False, "message": f"Table {table_name} not found"}

            with get_db_session() as session:
                query = session.query(model_class)
                
                # Apply filters if provided
                if filter_conditions:
                    # Simple filter implementation - can be enhanced
                    #query = query.filter(text(filter_conditions))
                    from sqlalchemy.sql import text as sql_text
                    query = query.filter(sql_text(filter_conditions))

                    

                    # Safe way to apply raw SQL filters
                    if filter_conditions:
                        query = query.filter(sql_text(filter_conditions))

                
                # Get total count
                total_count = query.count()
                
                # Apply pagination
                offset = (page - 1) * page_size
                #records = query.offset(offset).limit(page_size).all()
                print("SQL:", query.statement.compile(compile_kwargs={'literal_binds': True}))
                records = query.all()
                
                # Convert to dict list
                records_list = []
                for record in records:
                    record_dict = {}
                    for column in model_class.__table__.columns:
                        value = getattr(record, column.name)
                        if isinstance(value, datetime):
                            value = value.isoformat()
                        record_dict[column.name] = value
                    records_list.append(json.dumps(record_dict))
                
                return {
                    "success": True,
                    "message": f"Retrieved {len(records_list)} records",
                    "records": records_list,
                    "total_count": total_count
                }
        except Exception as e:
            logger.error("Failed to list records", table=table_name, error=str(e))
            return {"success": False, "message": f"Failed to list records: {str(e)}"}

    def run_migration(self, direction: str = "upgrade", target_revision: Optional[str] = None) -> Dict[str, Any]:
        """Run database migrations"""
        try:
            alembic_cfg = Config("alembic.ini")
            
            if direction == "upgrade":
                if target_revision:
                    command.upgrade(alembic_cfg, target_revision)
                else:
                    command.upgrade(alembic_cfg, "head")
            elif direction == "downgrade":
                if target_revision:
                    command.downgrade(alembic_cfg, target_revision)
                else:
                    command.downgrade(alembic_cfg, "-1")
            
            # Get current revision
            current_revision = self.get_current_revision()
            
            logger.info("Migration completed", direction=direction, current_revision=current_revision)
            return {
                "success": True,
                "message": f"Migration {direction} completed successfully",
                "current_revision": current_revision
            }
        except Exception as e:
            logger.error("Migration failed", direction=direction, error=str(e))
            return {"success": False, "message": f"Migration failed: {str(e)}"}

    def get_current_revision(self) -> str:
        """Get current database revision"""
        try:
            with engine.connect() as connection:
                context = MigrationContext.configure(connection)
                return context.get_current_revision() or "None"
        except Exception:
            return "Unknown"

    def get_migration_status(self) -> Dict[str, Any]:
        """Get current migration status"""
        try:
            current_revision = self.get_current_revision()
            
            # Get pending migrations
            alembic_cfg = Config("alembic.ini")
            script_dir = ScriptDirectory.from_config(alembic_cfg)
            
            with engine.connect() as connection:
                context = MigrationContext.configure(connection)
                pending = []
                
                for revision in script_dir.walk_revisions():
                    if revision.revision != current_revision:
                        pending.append(revision.revision)
                    else:
                        break
            
            return {
                "success": True,
                "current_revision": current_revision,
                "pending_migrations": pending
            }
        except Exception as e:
            logger.error("Failed to get migration status", error=str(e))
            return {"success": False, "message": f"Failed to get migration status: {str(e)}"}

    def add_column(self, table_name: str, column_name: str, column_type: str, nullable: bool = True, default_value: Optional[str] = None) -> Dict[str, Any]:
        """Add a column to an existing table"""
        try:
            with engine.connect() as connection:
                nullable_str = "NULL" if nullable else "NOT NULL"
                default_str = f"DEFAULT {default_value}" if default_value else ""
                
                sql = f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type} {nullable_str} {default_str}"
                connection.execute(text(sql))
                connection.commit()
                
                logger.info("Column added", table=table_name, column=column_name)
                return {"success": True, "message": f"Column {column_name} added to {table_name}"}
        except Exception as e:
            logger.error("Failed to add column", table=table_name, column=column_name, error=str(e))
            return {"success": False, "message": f"Failed to add column: {str(e)}"}

    def drop_column(self, table_name: str, column_name: str) -> Dict[str, Any]:
        """Drop a column from an existing table"""
        try:
            with engine.connect() as connection:
                sql = f"ALTER TABLE {table_name} DROP COLUMN {column_name}"
                connection.execute(text(sql))
                connection.commit()
                
                logger.info("Column dropped", table=table_name, column=column_name)
                return {"success": True, "message": f"Column {column_name} dropped from {table_name}"}
        except Exception as e:
            logger.error("Failed to drop column", table=table_name, column=column_name, error=str(e))
            return {"success": False, "message": f"Failed to drop column: {str(e)}"}

    def create_table(self, table_name: str, table_schema: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Create a table - either from existing model or from schema definition"""
        try:
            model_class = self.get_model_class(table_name)
            
            if model_class:
                # Create table from existing SQLAlchemy model
                model_class.__table__.create(engine, checkfirst=True)
                logger.info("Table created from model", table=table_name)
                return {"success": True, "message": f"Table {table_name} created successfully"}
            
            elif table_schema:
                # Create table from schema definition (for new tables)
                # This would require implementing schema parsing logic
                return {"success": False, "message": "Dynamic table creation from schema not implemented yet"}
            
            else:
                return {"success": False, "message": f"Table {table_name} not found in models and no schema provided"}
                
        except Exception as e:
            logger.error("Failed to create table", table=table_name, error=str(e))
            return {"success": False, "message": f"Failed to create table: {str(e)}"}

    def create_all_tables(self) -> Dict[str, Any]:
        """Create all tables defined in models"""
        try:
            Base.metadata.create_all(bind=engine, checkfirst=True)
            logger.info("All tables created successfully")
            return {"success": True, "message": "All tables created successfully"}
        except Exception as e:
            logger.error("Failed to create all tables", error=str(e))
            return {"success": False, "message": f"Failed to create all tables: {str(e)}"}

    def check_table_exists(self, table_name: str) -> bool:
        """Check if a table exists in the database"""
        try:
            inspector = inspect(engine)
            return table_name in inspector.get_table_names()
        except Exception:
            return False

    def health_check(self) -> Dict[str, Any]:
        """Perform health check"""
        try:
            with engine.connect() as connection:
                connection.execute(text("SELECT 1"))
                return {
                    "healthy": True,
                    "message": "Database connection healthy",
                    "version": "1.0.0"
                }
        except Exception as e:
            logger.error("Health check failed", error=str(e))
            return {
                "healthy": False,
                "message": f"Health check failed: {str(e)}",
                "version": "1.0.0"
            }
 
