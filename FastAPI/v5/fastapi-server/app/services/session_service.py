import json
import uuid
from typing import Optional, List
from datetime import datetime, timedelta
from app.proto import database_pb2, database_pb2_grpc
from app.schemas.user import UserSession
from app.core.config import settings
import grpc


class SessionService:
    def __init__(self, grpc_stub: database_pb2_grpc.DatabaseServiceStub, redis):
        self.stub = grpc_stub
        self.redis = redis

    async def create_session(self, user_id: int, access_token: str, 
                           refresh_token: str, user_agent: str = None, 
                           ip_address: str = None) -> UserSession:
        """Create a new user session"""
        session_token = str(uuid.uuid4())
        expires_at = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        
        # Store in database via gRPC
        session_data = {
            "user_id": user_id,
            "session_token": session_token,
            "expires_at": expires_at.isoformat(),
            "created_at": datetime.utcnow().isoformat(),
            "user_agent": user_agent,
            "ip_address": ip_address,
            "is_active": True
        }
        
        request = database_pb2.CreateRecordRequest(
            table_name="user_sessions",
            data=json.dumps(session_data)
        )
        response = await self.stub.CreateRecord(request)
        
        if response.success:
            session_data["id"] = response.record_id
            
            # Store tokens in Redis
            await self.redis.setex(
                f"session_tokens:{response.record_id}",
                settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
                json.dumps({
                    "access_token": access_token,
                    "refresh_token": refresh_token
                })
            )
            
            return UserSession(**session_data)
        else:
            raise Exception(f"Failed to create session: {response.message}")

    async def is_session_active(self, user_id: int, access_token: str) -> bool:
        """Check if session is active"""
        session_key = f"session:{user_id}:{access_token}"
        return await self.redis.exists(session_key)

    async def invalidate_session(self, user_id: int, access_token: str):
        """Invalidate a specific session"""
        session_key = f"session:{user_id}:{access_token}"
        await self.redis.delete(session_key)
        
        # Also mark as inactive in database
        # First find the session
        request = database_pb2.ListRecordsRequest(
            table_name="user_sessions",
            page=1,
            page_size=1,
            filter=json.dumps({"user_id": user_id, "is_active": True})
        )
        response = await self.stub.ListRecords(request)
        
        if response.success and response.records:
            session_data = json.loads(response.records[0])
            session_id = session_data["id"]
            
            # Update session to inactive
            update_request = database_pb2.UpdateRecordRequest(
                table_name="user_sessions",
                record_id=session_id,
                data=json.dumps({"is_active": False})
            )
            await self.stub.UpdateRecord(update_request)

    async def invalidate_all_user_sessions(self, user_id: int):
        """Invalidate all sessions for a user"""
        # Get all session keys for user
        pattern = f"session:{user_id}:*"
        keys = []
        async for key in self.redis.scan_iter(match=pattern):
            keys.append(key)
        
        if keys:
            await self.redis.delete(*keys)
        
        # Mark all sessions as inactive in database
        request = database_pb2.ListRecordsRequest(
            table_name="user_sessions",
            page=1,
            page_size=1000,  # Assuming a user won't have more than 1000 sessions
            filter=json.dumps({"user_id": user_id, "is_active": True})
        )
        response = await self.stub.ListRecords(request)
        
        if response.success:
            for record in response.records:
                session_data = json.loads(record)
                session_id = session_data["id"]
                
                update_request = database_pb2.UpdateRecordRequest(
                    table_name="user_sessions",
                    record_id=session_id,
                    data=json.dumps({"is_active": False})
                )
                await self.stub.UpdateRecord(update_request)

    async def get_user_sessions(self, user_id: int, active_only: bool = True) -> List[UserSession]:
        """Get all sessions for a user"""
        filter_data = {"user_id": user_id}
        if active_only:
            filter_data["is_active"] = True
        
        request = database_pb2.ListRecordsRequest(
            table_name="user_sessions",
            page=1,
            page_size=100,
            filter=json.dumps(filter_data)
        )
        response = await self.stub.ListRecords(request)
        
        sessions = []
        if response.success:
            for record in response.records:
                session_data = json.loads(record)
                sessions.append(UserSession(**session_data))
        
        return sessions

    async def get_session_tokens(self, session_id: str) -> Optional[dict]:
        """Get tokens for a session"""
        tokens = await self.redis.get(f"session_tokens:{session_id}")
        return json.loads(tokens) if tokens else None
