
# ================================
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Copy environment variables
COPY .env .env

# Generate protobuf files
RUN python -m grpc_tools.protoc -I./proto --python_out=./proto --grpc_python_out=./proto proto/database_service.proto

# Create non-root user
RUN useradd --create-home --shell /bin/bash app && chown -R app:app /app
USER app

# Expose port
EXPOSE 50051

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import grpc; import database_service_pb2_grpc; import database_service_pb2; \
    channel = grpc.insecure_channel('localhost:50051'); \
    stub = database_service_pb2_grpc.DatabaseServiceStub(channel); \
    response = stub.HealthCheck(database_service_pb2.HealthCheckRequest()); \
    exit(0 if response.healthy else 1)"

CMD ["python", "main.py"]

