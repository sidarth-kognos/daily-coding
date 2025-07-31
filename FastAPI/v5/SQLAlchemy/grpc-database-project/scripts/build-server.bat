@echo off
echo Building server Docker image...
cd server
docker build -t grpc-database-server:latest .
echo Server image built successfully
