@echo off
echo Generating protobuf files...

echo Generating server protobuf...
cd server
python -m grpc_tools.protoc -I./proto --python_out=. --grpc_python_out=. proto/database_service.proto

echo Generating client protobuf...
cd ../client
python -m grpc_tools.protoc -I./proto --python_out=. --grpc_python_out=. proto/database_service.proto

echo Protobuf generation complete
