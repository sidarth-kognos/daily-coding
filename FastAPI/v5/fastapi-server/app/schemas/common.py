from pydantic import BaseModel
from typing import Optional


class ResponseMessage(BaseModel):
    message: str
    success: bool = True


class HealthResponse(BaseModel):
    status: str
    version: str
    timestamp: str
