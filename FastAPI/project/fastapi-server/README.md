# FastAPI gRPC Server

A production-ready FastAPI server with gRPC database service integration, OAuth2 authentication, and Redis session management.

## Features

- **gRPC Database Integration**: All database operations via gRPC service
- **OAuth2 Authentication**: Identity provider integration
- **Session Management**: Redis-based scalable sessions
- **Security**: JWT tokens, password hashing, CORS
- **Dependency Injection**: Clean DI pattern
- **Multi-user Support**: Horizontal scaling capability

## Quick Start

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Generate gRPC Code**
   ```bash
   chmod +x generate_proto.sh
   ./generate_proto.sh
   ```

3. **Set Environment Variables**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

4. **Start Services**
   ```bash
   docker-compose up -d
   ```

5. **Run Application**
   ```bash
   uvicorn app.main:app --reload
   ```

## API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Project Structure

```
fastapi-server/
├── app/                 # Application code
│   ├── core/           # Core functionality
│   ├── api/            # API routes
│   ├── schemas/        # Pydantic models
│   ├── services/       # Business logic
│   └── proto/          # Generated gRPC code
├── proto/              # Protocol buffer definitions
├── tests/              # Test files
└── docker-compose.yml  # Container orchestration
```

## Environment Variables

See `.env.example` for all configuration options.

## Development

1. Generate proto code: `./generate_proto.sh`
2. Run tests: `pytest`
3. Format code: `black app/`
4. Type checking: `mypy app/`

## Deployment

Use the provided Dockerfile and docker-compose.yml for deployment.
