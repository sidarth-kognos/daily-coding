# gRPC Database Server Project

## Project Structure Created Successfully

```
grpc-database-project/
├── server/                    # gRPC Database Server
│   ├── app/
│   │   ├── models/           # SQLAlchemy models
│   │   ├── services/         # Business logic
│   │   ├── config.py         # Configuration
│   │   ├── database.py       # Database connection
│   │   └── grpc_server.py    # gRPC service implementation
│   ├── proto/                # Protocol Buffer definitions
│   ├── migrations/           # Alembic migrations
│   ├── k8s/                  # Kubernetes manifests
│   ├── requirements.txt      # Python dependencies
│   ├── Dockerfile           # Container build
│   └── main.py              # Application entry point
│
├── client/                   # gRPC Client and Tests
│   ├── client/              # Client library
│   ├── tests/               # Automated tests
│   ├── examples/            # Usage examples
│   ├── proto/               # Protocol Buffer definitions
│   ├── requirements_client.txt  # Client dependencies
│   └── run_tests.py         # Test runner
│
├── scripts/                 # Development scripts
└── docs/                    # Documentation
```

## Next Steps:

1. **Copy the code from Claude into the files:**
   - Copy server code into server/ files
   - Copy client code into client/ files
   - Copy proto definition into both proto/ folders

2. **Set up the development environment:**
   ```bash
   # Navigate to server directory
   cd server
   pip install -r requirements.txt
ECHO is off.
   # Navigate to client directory  
   cd ../client
   pip install -r requirements_client.txt
   ```

3. **Generate Protocol Buffer files:**
   ```bash
   # In server directory
   python -m grpc_tools.protoc -I./proto --python_out=. --grpc_python_out=. proto/database_service.proto
ECHO is off.
   # In client directory
   python -m grpc_tools.protoc -I./proto --python_out=. --grpc_python_out=. proto/database_service.proto
   ```

4. **Set up the database:**
   ```bash
   # In server directory
   alembic init migrations
   alembic revision --autogenerate -m "Initial migration"
   alembic upgrade head
   ```

5. **Run the server:**
   ```bash
   cd server
   python main.py
   ```

6. **Run the tests:**
   ```bash
   cd client
   python run_tests.py
   ```

## Development Scripts:

- `scripts/setup-dev.bat` - Set up development environment
- `scripts/build-server.bat` - Build server Docker image
- `scripts/run-tests.bat` - Run all tests
- `scripts/generate-proto.bat` - Generate protobuf files

## Environment Variables:

### Server (.env):
```
DATABASE_URL=mysql+pymysql://user:password@localhost:3306/database
GRPC_PORT=50051
LOG_LEVEL=INFO
MAX_WORKERS=10
DB_INIT_METHOD=migration
```

### Client (.env):
```
GRPC_SERVER_HOST=localhost
GRPC_SERVER_PORT=50051
GRPC_TIMEOUT=30
GRPC_MAX_RETRIES=3
```


# ================================
# Build and deployment instructions:
"""
# 1. Generate protobuf files:
python -m grpc_tools.protoc -I./proto --python_out=. --grpc_python_out=. proto/database_service.proto

# 2. Initialize Alembic (first time only):
alembic init migrations

# 3. Create initial migration:
alembic revision --autogenerate -m "Initial migration"

# 4. Build Docker image:
docker build -t your-registry/db-grpc-server:latest .

# 5. Push to registry:
docker push your-registry/db-grpc-server:latest

# 6. Deploy to Kubernetes:
kubectl apply -f k8s/

# 7. Table Creation Options:

## Option A: Automatic table creation on startup (default with migration)
# Tables will be created automatically when the server starts using Alembic migrations
# Set DB_INIT_METHOD=migration in ConfigMap (default)

## Option B: Direct table creation on startup 
# Set DB_INIT_METHOD=create_tables in ConfigMap
# This uses SQLAlchemy's create_all() method

## Option C: Manual migration after deployment
kubectl exec -it deployment/db-grpc-server -- python -c "
from app.services.db_service import DatabaseService
db_service = DatabaseService()
result = db_service.run_migration('upgrade')
print(result)
"

## Option D: Create individual tables via gRPC call
# Use the CreateTable gRPC method to create specific tables

# 8. Check if tables exist:
kubectl exec -it deployment/db-grpc-server -- python -c "
from app.services.db_service import DatabaseService
db_service = DatabaseService()
print('EMR_Cluster_Configuration exists:', db_service.check_table_exists('EMR_Cluster_Configuration'))
"

# 9. Database Schema Management:

## For production environments:
# - Use Alembic migrations (DB_INIT_METHOD=migration)
# - Version control your migrations
# - Test migrations in staging first

## For development/testing:
# - Can use direct table creation (DB_INIT_METHOD=create_tables)
# - Faster startup, but no migration history

## For existing databases:
# - Use Alembic stamp to mark current state
# - Then proceed with normal migrations
alembic stamp head

# 10. Monitoring table creation:
kubectl logs deployment/db-grpc-server | grep -i "table\|migration"
"""

