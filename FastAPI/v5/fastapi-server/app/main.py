from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from contextlib import asynccontextmanager
from datetime import datetime
from pydantic import BaseModel

from app.core.config import settings
from app.core.grpc_client import startup_grpc, shutdown_grpc
from app.api.v1 import auth, users, protected
import grpc
#from app.proto import database_service_pb2, database_service_pb2_grpc
from app.proto import database_pb2, database_pb2_grpc

from fastapi import Path, Query
from typing import Optional
from app.core.grpc_client import get_grpc_client


# Define request model for CreateRecord endpoint

class CreateRecordRequestModel(BaseModel):
    table_name: str
    data: str  # JSON string format expected as per your existing gRPC usage

class UpdateRecordRequestModel(BaseModel):
    table_name: str
    record_id: int
    data: str  # JSON string

class GetOrDeleteRequestModel(BaseModel):
    table_name: str
    record_id: int

class ListRecordsRequestModel(BaseModel):
    table_name: str
    page: Optional[int] = 1
    page_size: Optional[int] = 50
    filter_conditions: Optional[str] = None



@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: create gRPC channel and stub
    await startup_grpc()
    yield
    await shutdown_grpc()


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["localhost", "127.0.0.1", "*.yourdomain.com"]
)

app.add_middleware(GZipMiddleware, minimum_size=1000)

# Routes
app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])
app.include_router(users.router, prefix=f"{settings.API_V1_STR}/users", tags=["users"])
app.include_router(protected.router, prefix=f"{settings.API_V1_STR}/protected", tags=["protected"])


# ----------- gRPC Client Setup -------------

# If your startup_grpc sets these, import them accordingly;
# otherwise, create them here by connecting to your gRPC server.
# Example below creates channel & stub here:

#grpc_channel = grpc.insecure_channel('localhost:50051')
#grpc_stub = database_service_pb2_grpc.DatabaseServiceStub(grpc_channel)

from fastapi import Depends
from app.core.grpc_client import get_grpc_client

@app.post(f"{settings.API_V1_STR}/grpc/create_record")
async def create_record_via_grpc(
    request: CreateRecordRequestModel,
    grpc_client=Depends(get_grpc_client)
):
    try:
        stub = grpc_client.get_stub()
        #grpc_request = database_service_pb2.CreateRecordRequest(
        grpc_request = database_pb2.CreateRecordRequest(
            table_name=request.table_name,
            data=request.data
        )
        grpc_response = await stub.CreateRecord(grpc_request)

        return {
            "success": grpc_response.success,
            "message": grpc_response.message,
            "record_id": grpc_response.record_id
        }
    except grpc.aio.AioRpcError as e:
        raise HTTPException(status_code=500, detail=f"gRPC error: {e.details()}")

@app.get(f"{settings.API_V1_STR}/grpc/get_record")
async def get_record_via_grpc(
    table_name: str = Query(...),
    record_id: int = Query(...),
    grpc_client=Depends(get_grpc_client)
):
    try:
        stub = grpc_client.get_stub()
        grpc_request = database_pb2.GetRecordRequest(
            table_name=table_name,
            record_id=record_id
        )
        grpc_response = await stub.GetRecord(grpc_request)
        return {
            "success": grpc_response.success,
            "message": grpc_response.message,
            "data": grpc_response.data
        }
    except grpc.aio.AioRpcError as e:
        raise HTTPException(status_code=500, detail=f"gRPC error: {e.details()}")

@app.put(f"{settings.API_V1_STR}/grpc/update_record")
async def update_record_via_grpc(
    request: UpdateRecordRequestModel,
    grpc_client=Depends(get_grpc_client)
):
    try:
        stub = grpc_client.get_stub()
        grpc_request = database_pb2.UpdateRecordRequest(
            table_name=request.table_name,
            record_id=request.record_id,
            data=request.data
        )
        grpc_response = await stub.UpdateRecord(grpc_request)
        return {
            "success": grpc_response.success,
            "message": grpc_response.message
        }
    except grpc.aio.AioRpcError as e:
        raise HTTPException(status_code=500, detail=f"gRPC error: {e.details()}")

@app.delete(f"{settings.API_V1_STR}/grpc/delete_record")
async def delete_record_via_grpc(
    table_name: str = Query(...),
    record_id: int = Query(...),
    grpc_client=Depends(get_grpc_client)
):
    try:
        stub = grpc_client.get_stub()
        grpc_request = database_pb2.DeleteRecordRequest(
            table_name=table_name,
            record_id=record_id
        )
        grpc_response = await stub.DeleteRecord(grpc_request)
        return {
            "success": grpc_response.success,
            "message": grpc_response.message
        }
    except grpc.aio.AioRpcError as e:
        raise HTTPException(status_code=500, detail=f"gRPC error: {e.details()}")

@app.post(f"{settings.API_V1_STR}/grpc/list_records")
async def list_records_via_grpc(
    request: ListRecordsRequestModel,
    grpc_client=Depends(get_grpc_client)
):
    try:
        stub = grpc_client.get_stub()
        grpc_request = database_pb2.ListRecordsRequest(
            table_name=request.table_name,
            page=request.page,
            page_size=request.page_size,
            filter_conditions=request.filter_conditions or ""
        )
        grpc_response = await stub.ListRecords(grpc_request)
        return {
            "success": grpc_response.success,
            "message": grpc_response.message,
            "total_count": grpc_response.total_count,
            "records": list(grpc_response.records) if grpc_response.records else []
        }
    except grpc.aio.AioRpcError as e:
        raise HTTPException(status_code=500, detail=f"gRPC error: {e.details()}")

# If instead startup_grpc sets channel/stub, import and use those


# ------------ New FastAPI endpoint -------------
"""
@app.post(f"{settings.API_V1_STR}/grpc/create_record")
async def create_record_via_grpc(request: CreateRecordRequestModel):
    try:
        grpc_request = database_service_pb2.CreateRecordRequest(
            table_name=request.table_name,
            data=request.data
        )
        grpc_response = grpc_stub.CreateRecord(grpc_request)

        return {
            "success": grpc_response.success,
            "message": grpc_response.message,
            "record_id": grpc_response.record_id
        }
    except grpc.RpcError as e:
        # Handle gRPC errors, convert to HTTP error
        raise HTTPException(status_code=500, detail=f"gRPC error: {e.details()}")
"""

# ------------ Existing endpoints -------------

@app.get("/")
async def root():
    return {"message": f"Welcome to {settings.PROJECT_NAME}"}


@app.get("/health")
async def health_check():
    return {
        "status": "healthy", 
        "version": settings.VERSION,
        "timestamp": datetime.utcnow().isoformat()
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level="info"
    )
