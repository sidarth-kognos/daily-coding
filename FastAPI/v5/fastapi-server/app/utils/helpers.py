from typing import Optional, Dict, Any
import json
from datetime import datetime


def serialize_datetime(obj):
    """JSON serializer for datetime objects"""
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")


def safe_json_loads(data: str) -> Optional[Dict[Any, Any]]:
    """Safely load JSON data"""
    try:
        return json.loads(data)
    except (json.JSONDecodeError, TypeError):
        return None


def safe_json_dumps(data: Dict[Any, Any]) -> str:
    """Safely dump JSON data"""
    try:
        return json.dumps(data, default=serialize_datetime)
    except (TypeError, ValueError):
        return "{}"


def generate_username_from_email(email: str) -> str:
    """Generate username from email"""
    return email.split("@")[0].lower().replace(".", "_")


def validate_grpc_response(response) -> bool:
    """Validate gRPC response"""
    return hasattr(response, 'success') and response.success
