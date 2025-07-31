 # ================================
# client/config.py
import os
from typing import Optional

class ClientConfig:
    def __init__(self):
        self.server_host = os.getenv("GRPC_SERVER_HOST", "localhost")
        self.server_port = int(os.getenv("GRPC_SERVER_PORT", "50051"))
        self.timeout = int(os.getenv("GRPC_TIMEOUT", "30"))
        self.max_retries = int(os.getenv("GRPC_MAX_RETRIES", "3"))
        self.retry_delay = float(os.getenv("GRPC_RETRY_DELAY", "1.0"))
    
    @property
    def server_address(self) -> str:
        return f"{self.server_host}:{self.server_port}"

config = ClientConfig()
