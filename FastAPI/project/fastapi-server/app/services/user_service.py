import json
from typing import Optional, List
from app.proto import database_pb2, database_pb2_grpc
from app.schemas.user import UserCreate, UserUpdate, User
from app.core.security import get_password_hash, verify_password
from datetime import datetime
import grpc


class UserService:
    def __init__(self, grpc_stub: database_pb2_grpc.DatabaseServiceStub):
        self.stub = grpc_stub

    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
        try:
            request = database_pb2.GetRecordRequest(
                table_name="users",
                record_id=user_id
            )
            response = await self.stub.GetRecord(request)
            
            if response.success and response.data:
                user_data = json.loads(response.data)
                return User(**user_data)
            return None
        except grpc.RpcError:
            return None

    async def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        try:
            request = database_pb2.ListRecordsRequest(
                table_name="users",
                page=1,
                page_size=1,
                filter=json.dumps({"email": email})
            )
            response = await self.stub.ListRecords(request)
            
            if response.success and response.records:
                user_data = json.loads(response.records[0])
                return User(**user_data)
            return None
        except grpc.RpcError:
            return None

    async def get_user_by_username(self, username: str) -> Optional[User]:
        """Get user by username"""
        try:
            request = database_pb2.ListRecordsRequest(
                table_name="users",
                page=1,
                page_size=1,
                filter=json.dumps({"username": username})
            )
            response = await self.stub.ListRecords(request)
            
            if response.success and response.records:
                user_data = json.loads(response.records[0])
                return User(**user_data)
            return None
        except grpc.RpcError:
            return None

    async def get_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Get list of users"""
        try:
            page = (skip // limit) + 1
            request = database_pb2.ListRecordsRequest(
                table_name="users",
                page=page,
                page_size=limit
            )
            response = await self.stub.ListRecords(request)
            
            if response.success:
                users = []
                for record in response.records:
                    user_data = json.loads(record)
                    users.append(User(**user_data))
                return users
            return []
        except grpc.RpcError:
            return []

    async def create_user(self, user_create: UserCreate) -> User:
        """Create a new user"""
        hashed_password = get_password_hash(user_create.password)
        
        user_data = {
            "email": user_create.email,
            "username": user_create.username,
            "full_name": user_create.full_name,
            "hashed_password": hashed_password,
            "is_active": user_create.is_active,
            "is_superuser": False,
            "created_at": datetime.utcnow().isoformat(),
            "oauth_provider": None,
            "oauth_id": None
        }
        
        request = database_pb2.CreateRecordRequest(
            table_name="users",
            data=json.dumps(user_data)
        )
        response = await self.stub.CreateRecord(request)
        
        if response.success:
            user_data["id"] = response.record_id
            return User(**user_data)
        else:
            raise Exception(f"Failed to create user: {response.message}")

    async def update_user(self, user_id: int, user_update: UserUpdate) -> Optional[User]:
        """Update user"""
        # First get the existing user
        existing_user = await self.get_user_by_id(user_id)
        if not existing_user:
            return None
        
        # Update only the provided fields
        update_data = user_update.dict(exclude_unset=True)
        update_data["updated_at"] = datetime.utcnow().isoformat()
        
        request = database_pb2.UpdateRecordRequest(
            table_name="users",
            record_id=user_id,
            data=json.dumps(update_data)
        )
        response = await self.stub.UpdateRecord(request)
        
        if response.success:
            # Return updated user
            return await self.get_user_by_id(user_id)
        return None

    async def delete_user(self, user_id: int) -> bool:
        """Delete user"""
        try:
            request = database_pb2.DeleteRecordRequest(
                table_name="users",
                record_id=user_id
            )
            response = await self.stub.DeleteRecord(request)
            return response.success
        except grpc.RpcError:
            return False

    async def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """Authenticate user"""
        user = await self.get_user_by_email(email)
        if not user or not user.hashed_password:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    async def create_oauth_user(self, email: str, username: str, full_name: str, 
                               oauth_provider: str, oauth_id: str) -> User:
        """Create OAuth user"""
        user_data = {
            "email": email,
            "username": username,
            "full_name": full_name,
            "hashed_password": None,
            "oauth_provider": oauth_provider,
            "oauth_id": oauth_id,
            "is_active": True,
            "is_superuser": False,
            "created_at": datetime.utcnow().isoformat()
        }
        
        request = database_pb2.CreateRecordRequest(
            table_name="users",
            data=json.dumps(user_data)
        )
        response = await self.stub.CreateRecord(request)
        
        if response.success:
            user_data["id"] = response.record_id
            return User(**user_data)
        else:
            raise Exception(f"Failed to create OAuth user: {response.message}")
