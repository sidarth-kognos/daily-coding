@echo off
echo Setting up development environment...

echo [1/4] Installing server dependencies...
cd server
pip install -r requirements.txt

echo [2/4] Installing client dependencies...
cd ../client
pip install -r requirements_client.txt

echo [3/4] Generating protobuf files...
cd ../server
python -m grpc_tools.protoc -I./proto --python_out=. --grpc_python_out=. proto/database_service.proto
cd ../client
python -m grpc_tools.protoc -I./proto --python_out=. --grpc_python_out=. proto/database_service.proto

echo [4/4] Setting up database migrations...
cd ../server
alembic init migrations

echo Development environment setup complete
echo Next steps:
echo 1. Copy code from Claude into the files
echo 2. Update .env files with your database credentials
echo 3. Run: alembic revision --autogenerate -m "Initial migration"
echo 4. Run: python main.py
