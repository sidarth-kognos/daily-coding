import grpc
import asyncio
from typing import Optional
import redis.asyncio as aioredis
from app.core.config import settings
from app.proto import database_pb2_grpc


class GRPCDatabaseClient:
    def __init__(self):
        self.channel = None
        self.stub = None
    
    async def connect(self):
        """Establish gRPC connection"""
        if self.channel is None:
            self.channel = grpc.aio.insecure_channel(settings.GRPC_DATABASE_URL)
            self.stub = database_pb2_grpc.DatabaseServiceStub(self.channel)
    
    async def close(self):
        """Close gRPC connection"""
        if self.channel:
            await self.channel.close()
    
    def get_stub(self):
        """Get gRPC stub"""
        return self.stub


# Global gRPC client instance
grpc_client = GRPCDatabaseClient()

# Redis for session management
async_redis_client = aioredis.from_url(settings.REDIS_URL, decode_responses=True)


# Dependency to get gRPC client
async def get_grpc_client():
    if grpc_client.stub is None:
        await grpc_client.connect()
    return grpc_client


# Dependency to get Redis session
async def get_redis():
    return async_redis_client


# Startup and shutdown handlers
async def startup_grpc():
    await grpc_client.connect()


async def shutdown_grpc():
    await grpc_client.close()
