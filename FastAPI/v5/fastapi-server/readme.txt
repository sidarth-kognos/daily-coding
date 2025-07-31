D:\Source\FastAPI>python -X utf8 fastapi_generator.py
Creating FastAPI gRPC Server Project...

Creating directory structure...

Creating project files...
Created: fastapi-server\app\core\config.py
Created: fastapi-server\app\core\grpc_client.py
Created: fastapi-server\app\core\security.py
Created: fastapi-server\app\core\dependencies.py
Created: fastapi-server\app\schemas\user.py
Created: fastapi-server\app\schemas\auth.py
Created: fastapi-server\app\schemas\common.py
Created: fastapi-server\app\services\user_service.py
Created: fastapi-server\app\services\session_service.py
Created: fastapi-server\app\services\auth_service.py
Created: fastapi-server\app\api\v1\auth.py
Created: fastapi-server\app\api\v1\users.py
Created: fastapi-server\app\api\v1\protected.py
Created: fastapi-server\app\main.py
Created: fastapi-server\app\utils\helpers.py
Created: fastapi-server\proto\database.proto
Created: fastapi-server\requirements.txt
Created: fastapi-server\.env.example
Created: fastapi-server\docker-compose.yml
Created: fastapi-server\Dockerfile
Created: fastapi-server\generate_proto.sh
Created: fastapi-server\tests\test_main.py
Created: fastapi-server\README.md

Making scripts executable...
Made executable: fastapi-server\generate_proto.sh

Creating proto placeholders...
Created placeholder: fastapi-server\app\proto\database_pb2.py
Created placeholder: fastapi-server\app\proto\database_pb2_grpc.py

FastAPI gRPC Server project created successfully!

Next steps:
1. cd fastapi-server
2. pip install -r requirements.txt
3. ./generate_proto.sh  # Generate gRPC code
4. cp .env.example .env  # Configure environment
5. docker-compose up -d  # Start services
6. uvicorn app.main:app --reload  # Run the server

Server will be available at: http://localhost:8000
API docs will be at: http://localhost:8000/docs
