#!/bin/bash

# Generate Python gRPC code from proto files
python -m grpc_tools.protoc \
    -I./proto \
    --python_out=./app/proto \
    --grpc_python_out=./app/proto \
    ./proto/database.proto

echo "gRPC code generated successfully!"
