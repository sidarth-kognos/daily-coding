# ================================
# app/models/tables.py
from sqlalchemy import Column, Integer, BigInteger, String, Text, DateTime, Float, JSON, ForeignKey
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class EMRClusterConfiguration(Base):
    __tablename__ = 'EMR_Cluster_Configuration'
    
    id = Column(BigInteger, primary_key=True)
    cluster_config = Column(String(255), nullable=False)
    cluster_id = Column(String(255), nullable=True)
    cluster_name = Column(String(255), nullable=False)
    cluster_type = Column(String(255), nullable=True)
    created_by = Column(String(255), nullable=False)
    idle_time = Column(Integer, nullable=False)
    status = Column(String(255), nullable=True)
    updation_time_stamp = Column(DateTime(6), nullable=True)
    worker_core = Column(Integer, nullable=False)
    core_cluster_size = Column(String(255), nullable=True)
    worker_primary = Column(Integer, nullable=False)
    primary_cluster_size = Column(String(255), nullable=True)

class EMRJobRunsStatus(Base):
    __tablename__ = 'emr_job_runs_status'
    
    id = Column(BigInteger, primary_key=True)
    duration = Column(String(255), nullable=True)
    end_time = Column(String(255), nullable=True)
    job_id = Column(Integer, nullable=True)
    job_name = Column(String(255), nullable=False)
    label = Column(String(255), nullable=True)
    log_info = Column(String(10000), nullable=True)
    run_id = Column(String(255), nullable=True)
    start_time = Column(String(255), nullable=True)
    status = Column(String(255), nullable=True)
    parent_run_label = Column(String(255), nullable=True)

class EMRJobSettings(Base):
    __tablename__ = 'emr_job_settings'
    
    id = Column(BigInteger, primary_key=True)
    cluster_id = Column(String(255), nullable=True)
    job_name = Column(String(255), nullable=False)
    job_prefix = Column(String(255), nullable=False)
    parameter_json = Column(LONGTEXT, nullable=False)
    script_path = Column(String(255), nullable=False)

class IQMeteringDataProcessedRecords(Base):
    __tablename__ = 'iq_metering_data_processed_records'
    
    id = Column(BigInteger, primary_key=True)
    data_size_mb = Column(Float, nullable=True)
    data_source = Column(String(1000), nullable=True)
    data_type = Column(String(255), nullable=True)
    metering_event_id = Column(String(255), nullable=True)
    metering_event_status = Column(String(255), nullable=True)
    object_kind = Column(String(255), nullable=True)
    object_type = Column(String(255), nullable=True)
    operation_type = Column(String(255), nullable=True)
    osdu_object_id = Column(String(255), nullable=True)
    partition_id = Column(String(255), nullable=True)
    process_step = Column(String(255), nullable=True)
    repository_url = Column(String(1000), nullable=True)
    status = Column(String(255), nullable=True)
    timestamp = Column(DateTime(6), nullable=True)
    user = Column(String(255), nullable=True)

class IQMeteringEventSummaryRecords(Base):
    __tablename__ = 'iq_metering_event_summary_records'
    
    id = Column(BigInteger, primary_key=True)
    dimension = Column(String(255), nullable=True)
    metering_event_id = Column(String(255), nullable=True)
    metering_event_summary = Column(LONGTEXT, nullable=True)
    provider_account_id = Column(String(255), nullable=True)
    timestamp = Column(DateTime(6), nullable=True)

class IQMeteringObjectRecords(Base):
    __tablename__ = 'iq_metering_object_records'
    
    id = Column(BigInteger, primary_key=True)
    data_type = Column(String(255), nullable=True)
    metering_event_id = Column(String(255), nullable=True)
    metering_event_status = Column(String(255), nullable=True)
    object_kind = Column(String(255), nullable=True)
    object_type = Column(String(255), nullable=True)
    operation_type = Column(String(255), nullable=True)
    osdu_object_id = Column(String(255), nullable=True)
    partition_id = Column(String(255), nullable=True)
    process_step = Column(String(255), nullable=True)
    repository_url = Column(String(1000), nullable=True)
    status = Column(String(255), nullable=True)
    timestamp = Column(DateTime(6), nullable=True)
    user = Column(String(255), nullable=True)

class JobDataSelection(Base):
    __tablename__ = 'job_data_selection'
    
    id = Column(BigInteger, primary_key=True)
    data_selection = Column(String(255), nullable=True)
    data_type = Column(String(255), nullable=True)
    job_id = Column(String(255), nullable=True)
    job_type = Column(String(255), nullable=True)
    json_parameter = Column(String(255), nullable=True)
    run_id = Column(String(255), nullable=True)
    timestamp = Column(String(255), nullable=True)
    useremail = Column(String(255), nullable=True)

class OSDUInstanceSettings(Base):
    __tablename__ = 'osdu_instance_settings'
    
    id = Column(BigInteger, primary_key=True)
    authentication_token = Column(LONGTEXT, nullable=True)
    clientid = Column(LONGTEXT, nullable=False)
    clientsecret = Column(LONGTEXT, nullable=False)
    cloud_type = Column(String(255), nullable=False)
    connection_name = Column(String(255), nullable=False)
    data_partition_id = Column(String(255), nullable=False)
    endpointurl = Column(LONGTEXT, nullable=True)
    grant_type = Column(String(255), nullable=True)
    instance_id = Column(String(255), nullable=False)
    member = Column(LONGTEXT, nullable=True)
    osdu_version = Column(String(255), nullable=False)
    password = Column(LONGTEXT, nullable=True)
    region = Column(String(255), nullable=True)
    scope = Column(LONGTEXT, nullable=True)
    tenant_id = Column(LONGTEXT, nullable=True)
    token_url = Column(String(255), nullable=True)
    type = Column(String(255), nullable=False)
    url = Column(String(255), nullable=False)
    username = Column(LONGTEXT, nullable=True)

class OSDUUsageStatistics(Base):
    __tablename__ = 'osdu_usage_statistics'
    
    id = Column(BigInteger, primary_key=True)
    data_json = Column(LONGTEXT, nullable=False)
    data_partition_id = Column(String(255), nullable=False)
    datatype = Column(String(255), nullable=False)
    object_type = Column(String(255), nullable=False)
    osdu_id = Column(String(255), nullable=False)
    osdu_query_type = Column(String(255), nullable=False)
    osdu_url = Column(String(255), nullable=False)
    timestamp = Column(String(255), nullable=True)
    url_endpoint = Column(String(255), nullable=False)
    user = Column(String(255), nullable=False)

class OSDUUserToken(Base):
    __tablename__ = 'osdu_user_token'
    
    id = Column(BigInteger, primary_key=True)
    access_token = Column(LONGTEXT, nullable=False)
    client_id = Column(LONGTEXT, nullable=False)
    client_secret = Column(LONGTEXT, nullable=False)
    last_updated_on = Column(DateTime(6), nullable=False)
    refresh_token = Column(LONGTEXT, nullable=False)
    token_url = Column(LONGTEXT, nullable=False)
    user_id = Column(String(255), nullable=False)

class ProjectSettings(Base):
    __tablename__ = 'project_settings'
    
    id = Column(BigInteger, primary_key=True)
    description = Column(String(255), nullable=True)
    lastModifiedDate = Column(DateTime(6), nullable=True)
    osduId = Column(String(255), nullable=True)
    projectName = Column(String(255), nullable=True)
    projectSettings = Column(LONGTEXT, nullable=True)
    projectType = Column(String(255), nullable=True)
    userEmail = Column(String(255), nullable=True)

class RBACModuleInfo(Base):
    __tablename__ = 'rbac_module_info'
    
    id = Column(BigInteger, primary_key=True)
    created_at = Column(DateTime(6), nullable=True)
    module_description = Column(String(255), nullable=True)
    module_key = Column(String(255), nullable=False)
    module_level = Column(Integer, nullable=True)
    module_name = Column(String(255), nullable=False)
    path = Column(String(255), nullable=True)
    updated_at = Column(DateTime(6), nullable=True)
    parent_id = Column(BigInteger, ForeignKey('rbac_module_info.id'), nullable=True)
    
    # Self-referential relationship
    children = relationship("RBACModuleInfo", backref="parent", remote_side=[id])

class RBACRoleCategory(Base):
    __tablename__ = 'rbac_role_category'
    
    id = Column(BigInteger, primary_key=True)
    category_name = Column(String(255), nullable=False)
    created_at = Column(DateTime(6), nullable=True)
    updated_at = Column(DateTime(6), nullable=True)

class RBACRoleInfo(Base):
    __tablename__ = 'rbac_role_info'
    
    id = Column(BigInteger, primary_key=True)
    created_at = Column(DateTime(6), nullable=True)
    role_description = Column(String(255), nullable=True)
    role_name = Column(String(255), nullable=False)
    updated_at = Column(DateTime(6), nullable=True)
    category_id = Column(BigInteger, ForeignKey('rbac_role_category.id'), nullable=False)
    
    category = relationship("RBACRoleCategory", backref="roles")

class RBACRoleModulePermission(Base):
    __tablename__ = 'rbac_role_module_permission'
    
    id = Column(BigInteger, primary_key=True)
    created_at = Column(DateTime(6), nullable=True)
    permission = Column(String(255), nullable=False)
    updated_at = Column(DateTime(6), nullable=True)
    module_id = Column(BigInteger, ForeignKey('rbac_module_info.id'), nullable=False)
    role_id = Column(BigInteger, ForeignKey('rbac_role_info.id'), nullable=False)
    
    module = relationship("RBACModuleInfo", backref="permissions")
    role = relationship("RBACRoleInfo", backref="permissions")

class RBACRoleSettings(Base):
    __tablename__ = 'rbac_role_settings'
    
    id = Column(Integer, primary_key=True)
    role_id = Column(Integer, nullable=False)
    role_settings = Column(JSON, nullable=False)

class RBACUserInfo(Base):
    __tablename__ = 'rbac_user_info'
    
    id = Column(BigInteger, primary_key=True)
    created_at = Column(DateTime(6), nullable=True)
    email = Column(String(255), nullable=False)
    first_name = Column(String(255), nullable=True)
    last_name = Column(String(255), nullable=True)
    updated_at = Column(DateTime(6), nullable=True)

class RBACUserRoleAssignment(Base):
    __tablename__ = 'rbac_user_role_assignment'
    
    id = Column(BigInteger, primary_key=True)
    created_at = Column(DateTime(6), nullable=True)
    updated_at = Column(DateTime(6), nullable=True)
    role_id = Column(BigInteger, ForeignKey('rbac_role_info.id'), nullable=False)
    user_id = Column(BigInteger, ForeignKey('rbac_user_info.id'), nullable=False)
    
    role = relationship("RBACRoleInfo", backref="user_assignments")
    user = relationship("RBACUserInfo", backref="role_assignments")

class SegyScanData(Base):
    __tablename__ = 'segy_scan_data'
    
    id = Column(BigInteger, primary_key=True)
    bin_header = Column(Text, nullable=True)
    comment = Column(Text, nullable=True)
    curated_info = Column(Text, nullable=True)
    is_2d = Column(TINYINT, nullable=True)
    num_traces = Column(Integer, nullable=True)
    parsed_text_header = Column(Text, nullable=True)
    pri_byte = Column(String(255), nullable=True)
    result = Column(String(255), nullable=True)
    sec_byte = Column(String(255), nullable=True)
    segy_data_type = Column(String(255), nullable=True)
    segy_path = Column(String(255), nullable=False)
    text_header = Column(Text, nullable=True)
    timestamp = Column(String(255), nullable=True)
    user_defined_info = Column(Text, nullable=True)
    x_byte = Column(String(255), nullable=True)
    xy_scalar = Column(Float, nullable=True)
    y_byte = Column(String(255), nullable=True)

class SegyToVdsInfo(Base):
    __tablename__ = 'segy_to_vds_info'
    
    filename = Column(String(255), primary_key=True)
    pod_id = Column(Integer, nullable=False)
    request_data = Column(LONGTEXT, nullable=True)

class SegyToVdsStatus(Base):
    __tablename__ = 'segy_to_vds_status'
    
    id = Column(BigInteger, primary_key=True)
    end_time = Column(DateTime(6), nullable=True)
    filename = Column(String(1000), nullable=True)
    file_size = Column(BigInteger, nullable=True)
    input_file_path = Column(String(1000), nullable=True)
    job_name = Column(String(255), nullable=True)
    namespace = Column(String(255), nullable=True)
    node_name = Column(String(255), nullable=True)
    pod_id = Column(String(255), nullable=True)
    pod_uid = Column(String(255), nullable=False)
    progress = Column(Float, nullable=True)
    request_data = Column(String(10000), nullable=True)
    start_time = Column(DateTime(6), nullable=True)
    status = Column(String(255), nullable=True)
    textual_header = Column(LONGTEXT, nullable=True)
    thread_id = Column(String(255), nullable=False)
    time_taken = Column(String(255), nullable=True)
    time_taken_seconds = Column(Float, nullable=True)
    vds_path = Column(String(255), nullable=True)

class SettingsAppRegistration(Base):
    __tablename__ = 'settings_app_registration'
    
    id = Column(BigInteger, primary_key=True)
    app_name = Column(String(255), nullable=True)
    settings = Column(LONGTEXT, nullable=True)

class SettingsDeTree(Base):
    __tablename__ = 'settings_de_tree'
    
    id = Column(BigInteger, primary_key=True)
    json_data = Column(LONGTEXT, nullable=False)
    product = Column(String(255), nullable=False)

class SettingsUserLogging(Base):
    __tablename__ = 'settings_user_logging'
    
    id = Column(BigInteger, primary_key=True)
    activity = Column(String(255), nullable=True)
    time_stamp = Column(String(255), nullable=True)
    user = Column(String(255), nullable=True)

class UserSettings(Base):
    __tablename__ = 'user_settings'
    
    id = Column(BigInteger, primary_key=True)
    settings = Column(LONGTEXT, nullable=True)
    updationTimeStamp = Column(String(255), nullable=True)
    username = Column(String(255), nullable=False)

class EmployeeInfo(Base):
    __tablename__ = 'employee_info'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    department = Column(String(100), nullable=True)
    salary = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class user(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)


