"""# ================================
# app/config.py
import os
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    database_url: str = os.getenv(
        "DATABASE_URL", 
        "mysql+pymysql://root:mysql@localhost:3306/testdbsid"
    )
    grpc_port: int = int(os.getenv("GRPC_PORT", "50051"))
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    max_workers: int = int(os.getenv("MAX_WORKERS", "10"))
    
    class Config:
        env_file = ".env"

settings = Settings()

"""




# app/config.py — Using Pydantic
from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    #SQLALCHEMY_DATABASE_URL: str = "mysql+pymysql://root:mysql@localhost:3306/dev_db"
    #SQLALCHEMY_DATABASE_URL: str = "mysql+pymysql://root:mysql@localhost:3306/running_db"
    #database_url: str = Field(default=SQLALCHEMY_DATABASE_URL)
    #original
    #database_url: str = Field(default="mysql+pymysql://root:mysql@localhost:3306/testdbsid")
    # For dev DB
    database_url: str = Field(default="mysql+pymysql://root:mysql@localhost:3306/dev_db")
    # For running DB
    #database_url: str = Field(default="mysql+pymysql://root:mysql@localhost:3306/running_db")
    grpc_port: int = Field(default=50051)
    log_level: str = Field(default="INFO")
    max_workers: int = Field(default=10)

    class Config:
        env_file = ".env"

settings = Settings()
