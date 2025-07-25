from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from contextlib import asynccontextmanager
from datetime import datetime

from app.core.config import settings
from app.core.grpc_client import startup_grpc, shutdown_grpc
from app.api.v1 import auth, users, protected


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await startup_grpc()
    yield
    # Shutdown
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
