@echo off
setlocal enabledelayedexpansion

echo ================================
echo   gRPC Database Server Project
echo   Folder Structure Creator
echo ================================
echo.

REM Get the current directory as the base path
set BASE_DIR=%CD%
echo Creating project in: %BASE_DIR%
echo.

REM Create main project directories
echo [1/4] Creating main project directories...
mkdir "grpc-database-project" 2>nul
cd "grpc-database-project"

REM ================================
REM SERVER STRUCTURE
REM ================================
echo [2/4] Creating server structure...

REM Server main directories
mkdir "server" 2>nul
mkdir "server\app" 2>nul
mkdir "server\app\models" 2>nul
mkdir "server\app\services" 2>nul
mkdir "server\proto" 2>nul
mkdir "server\migrations" 2>nul
mkdir "server\k8s" 2>nul

REM Server Python files
echo. > "server\app\__init__.py"
echo. > "server\app\config.py"
echo. > "server\app\database.py"
echo. > "server\app\grpc_server.py"
echo. > "server\app\models\__init__.py"
echo. > "server\app\models\tables.py"
echo. > "server\app\services\__init__.py"
echo. > "server\app\services\db_service.py"
echo. > "server\main.py"

REM Server configuration files
echo. > "server\requirements.txt"
echo. > "server\alembic.ini"
echo. > "server\Dockerfile"
echo. > "server\.env"

REM Server proto files
echo. > "server\proto\database_service.proto"

REM Server k8s files
echo. > "server\k8s\deployment.yaml"
echo. > "server\k8s\service.yaml"
echo. > "server\k8s\configmap.yaml"

REM Server migration placeholder
echo. > "server\migrations\README.md"

REM ================================
REM CLIENT STRUCTURE
REM ================================
echo [3/4] Creating client structure...

REM Client main directories
mkdir "client" 2>nul
mkdir "client\client" 2>nul
mkdir "client\proto" 2>nul
mkdir "client\tests" 2>nul
mkdir "client\examples" 2>nul

REM Client Python files
echo. > "client\client\__init__.py"
echo. > "client\client\config.py"
echo. > "client\client\db_client.py"
echo. > "client\client\test_client.py"

REM Client test files
echo. > "client\tests\__init__.py"
echo. > "client\tests\test_crud.py"
echo. > "client\tests\test_migrations.py"
echo. > "client\tests\test_schema.py"

REM Client example files
echo. > "client\examples\__init__.py"
echo. > "client\examples\basic_usage.py"
echo. > "client\examples\migration_example.py"
echo. > "client\examples\bulk_operations.py"

REM Client configuration files
echo. > "client\requirements_client.txt"
echo. > "client\run_tests.py"
echo. > "client\.env"

REM Client proto files (shared with server)
echo. > "client\proto\database_service.proto"

REM ================================
REM SHARED DOCUMENTATION
REM ================================
echo [4/4] Creating documentation and shared files...

REM Project documentation
echo. > "README.md"
echo. > "SETUP.md"
echo. > ".gitignore"
echo. > "docker-compose.yml"

REM Development scripts
mkdir "scripts" 2>nul
echo. > "scripts\setup-dev.bat"
echo. > "scripts\build-server.bat"
echo. > "scripts\run-tests.bat"
echo. > "scripts\generate-proto.bat"

REM ================================
REM CREATE SETUP INSTRUCTIONS
REM ================================
echo [INFO] Creating setup instructions...

(
echo # gRPC Database Server Project
echo.
echo ## Project Structure Created Successfully!
echo.
echo ```
echo grpc-database-project/
echo ├── server/                    # gRPC Database Server
echo │   ├── app/
echo │   │   ├── models/           # SQLAlchemy models
echo │   │   ├── services/         # Business logic
echo │   │   ├── config.py         # Configuration
echo │   │   ├── database.py       # Database connection
echo │   │   └── grpc_server.py    # gRPC service implementation
echo │   ├── proto/                # Protocol Buffer definitions
echo │   ├── migrations/           # Alembic migrations
echo │   ├── k8s/                  # Kubernetes manifests
echo │   ├── requirements.txt      # Python dependencies
echo │   ├── Dockerfile           # Container build
echo │   └── main.py              # Application entry point
echo │
echo ├── client/                   # gRPC Client and Tests
echo │   ├── client/              # Client library
echo │   ├── tests/               # Automated tests
echo │   ├── examples/            # Usage examples
echo │   ├── proto/               # Protocol Buffer definitions
echo │   ├── requirements_client.txt  # Client dependencies
echo │   └── run_tests.py         # Test runner
echo │
echo ├── scripts/                 # Development scripts
echo └── docs/                    # Documentation
echo ```
echo.
echo ## Next Steps:
echo.
echo 1. **Copy the code from Claude into the files:**
echo    - Copy server code into server/ files
echo    - Copy client code into client/ files
echo    - Copy proto definition into both proto/ folders
echo.
echo 2. **Set up the development environment:**
echo    ```bash
echo    # Navigate to server directory
echo    cd server
echo    pip install -r requirements.txt
echo    
echo    # Navigate to client directory  
echo    cd ../client
echo    pip install -r requirements_client.txt
echo    ```
echo.
echo 3. **Generate Protocol Buffer files:**
echo    ```bash
echo    # In server directory
echo    python -m grpc_tools.protoc -I./proto --python_out=. --grpc_python_out=. proto/database_service.proto
echo    
echo    # In client directory
echo    python -m grpc_tools.protoc -I./proto --python_out=. --grpc_python_out=. proto/database_service.proto
echo    ```
echo.
echo 4. **Set up the database:**
echo    ```bash
echo    # In server directory
echo    alembic init migrations
echo    alembic revision --autogenerate -m "Initial migration"
echo    alembic upgrade head
echo    ```
echo.
echo 5. **Run the server:**
echo    ```bash
echo    cd server
echo    python main.py
echo    ```
echo.
echo 6. **Run the tests:**
echo    ```bash
echo    cd client
echo    python run_tests.py
echo    ```
echo.
echo ## Development Scripts:
echo.
echo - `scripts/setup-dev.bat` - Set up development environment
echo - `scripts/build-server.bat` - Build server Docker image
echo - `scripts/run-tests.bat` - Run all tests
echo - `scripts/generate-proto.bat` - Generate protobuf files
echo.
echo ## Environment Variables:
echo.
echo ### Server (.env^):
echo ```
echo DATABASE_URL=mysql+pymysql://user:password@localhost:3306/database
echo GRPC_PORT=50051
echo LOG_LEVEL=INFO
echo MAX_WORKERS=10
echo DB_INIT_METHOD=migration
echo ```
echo.
echo ### Client (.env^):
echo ```
echo GRPC_SERVER_HOST=localhost
echo GRPC_SERVER_PORT=50051
echo GRPC_TIMEOUT=30
echo GRPC_MAX_RETRIES=3
echo ```
) > "README.md"

REM ================================
REM CREATE DEVELOPMENT SCRIPTS
REM ================================

REM Setup development environment script
(
echo @echo off
echo echo Setting up development environment...
echo.
echo echo [1/4] Installing server dependencies...
echo cd server
echo pip install -r requirements.txt
echo.
echo echo [2/4] Installing client dependencies...
echo cd ../client
echo pip install -r requirements_client.txt
echo.
echo echo [3/4] Generating protobuf files...
echo cd ../server
echo python -m grpc_tools.protoc -I./proto --python_out=. --grpc_python_out=. proto/database_service.proto
echo cd ../client
echo python -m grpc_tools.protoc -I./proto --python_out=. --grpc_python_out=. proto/database_service.proto
echo.
echo echo [4/4] Setting up database migrations...
echo cd ../server
echo alembic init migrations
echo.
echo echo Development environment setup complete!
echo echo Next steps:
echo echo 1. Copy code from Claude into the files
echo echo 2. Update .env files with your database credentials
echo echo 3. Run: alembic revision --autogenerate -m "Initial migration"
echo echo 4. Run: python main.py
) > "scripts\setup-dev.bat"

REM Build server script
(
echo @echo off
echo echo Building server Docker image...
echo cd server
echo docker build -t grpc-database-server:latest .
echo echo Server image built successfully!
) > "scripts\build-server.bat"

REM Run tests script
(
echo @echo off
echo echo Running client tests...
echo cd client
echo python run_tests.py
) > "scripts\run-tests.bat"

REM Generate proto script
(
echo @echo off
echo echo Generating protobuf files...
echo.
echo echo Generating server protobuf...
echo cd server
echo python -m grpc_tools.protoc -I./proto --python_out=. --grpc_python_out=. proto/database_service.proto
echo.
echo echo Generating client protobuf...
echo cd ../client
echo python -m grpc_tools.protoc -I./proto --python_out=. --grpc_python_out=. proto/database_service.proto
echo.
echo echo Protobuf generation complete!
) > "scripts\generate-proto.bat"

REM ================================
REM CREATE GITIGNORE
REM ================================
(
echo # Python
echo __pycache__/
echo *.py[cod]
echo *$py.class
echo *.so
echo .Python
echo build/
echo develop-eggs/
echo dist/
echo downloads/
echo eggs/
echo .eggs/
echo lib/
echo lib64/
echo parts/
echo sdist/
echo var/
echo wheels/
echo *.egg-info/
echo .installed.cfg
echo *.egg
echo.
echo # Virtual Environments
echo venv/
echo env/
echo ENV/
echo.
echo # IDE
echo .vscode/
echo .idea/
echo *.swp
echo *.swo
echo *~
echo.
echo # Environment Variables
echo .env
echo .env.local
echo.
echo # Database
echo *.db
echo *.sqlite
echo.
echo # Logs
echo *.log
echo logs/
echo.
echo # Docker
echo .dockerignore
echo.
echo # Generated Files
echo *_pb2.py
echo *_pb2_grpc.py
echo.
echo # Alembic
echo migrations/versions/
echo.
echo # OS
echo .DS_Store
echo Thumbs.db
echo.
echo # Pytest
echo .pytest_cache/
echo .coverage
echo htmlcov/
) > ".gitignore"

REM ================================
REM CREATE DOCKER COMPOSE
REM ================================
(
echo version: '3.8'
echo.
echo services:
echo   mysql:
echo     image: mysql:8.0
echo     environment:
echo       MYSQL_ROOT_PASSWORD: rootpassword
echo       MYSQL_DATABASE: testdb
echo       MYSQL_USER: testuser
echo       MYSQL_PASSWORD: testpassword
echo     ports:
echo       - "3306:3306"
echo     volumes:
echo       - mysql_data:/var/lib/mysql
echo.
echo   db-server:
echo     build:
echo       context: ./server
echo       dockerfile: Dockerfile
echo     depends_on:
echo       - mysql
echo     environment:
echo       DATABASE_URL: mysql+pymysql://testuser:testpassword@mysql:3306/testdb
echo       GRPC_PORT: 50051
echo       LOG_LEVEL: INFO
echo     ports:
echo       - "50051:50051"
echo.
echo volumes:
echo   mysql_data:
) > "docker-compose.yml"

REM ================================
REM FINAL SUMMARY
REM ================================
echo.
echo ================================
echo   PROJECT CREATED SUCCESSFULLY!
echo ================================
echo.
echo Project location: %CD%
echo.
echo Structure created:
echo   ✓ Server application (server/)
echo   ✓ Client library and tests (client/)
echo   ✓ Development scripts (scripts/)
echo   ✓ Documentation files
echo   ✓ Docker configuration
echo.
echo Next steps:
echo   1. Copy code from Claude artifacts into the created files
echo   2. Run: scripts\setup-dev.bat
echo   3. Update .env files with your database credentials
echo   4. Follow the README.md instructions
echo.
echo Happy coding! 🚀

REM Show the directory structure
echo.
echo Directory structure:
tree /F

pause