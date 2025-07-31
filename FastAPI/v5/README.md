# 📦 FastAPI + gRPC Integration

This repository is a **quickstart and safety guide** for integrating **FastAPI** with a **gRPC server** to perform **CRUD operations on a MySQL database**.

---

## 🚀 Getting Started

This guide walks you through setting up two components:

- A **gRPC server** for handling database operations  
- A **FastAPI client** for serving a web UI

> ⚠️ No Docker setup is used in this guide.

---

## 📂 Initial Setup

1. Copy the `fastapi` and `mysqlalchemy` folders from `prototypes/python`.
2. Open each folder in a separate VSCode window.
3. When the setup is complete, you'll be running **two separate servers**, one per window.

---

## 🛠️ Setting Up the gRPC Server

### 1. Create and activate a virtual environment

```bash
py -3.10 -m venv venv
venv\Scripts\activate
```

### 2. Generate the protobuf files

```bash
cd server

python -m grpc_tools.protoc -I./proto --python_out=. --grpc_python_out=. proto/database_service.proto

cd ../client

python -m grpc_tools.protoc -I./proto --python_out=. --grpc_python_out=. proto/database_service.proto
```

### 3. Run the gRPC server

```bash
cd server
python main.py
```

### 4. Test the gRPC server using `grpcurl`

Open a **new terminal** and run:

```bash
cd server

grpcurl -plaintext localhost:50051 list
grpcurl -plaintext localhost:50051 describe database.DatabaseService
grpcurl -plaintext -d "{}" localhost:50051 database.DatabaseService.HealthCheck
grpcurl -plaintext -d "{\"tableName\": \"user\"}" localhost:50051 database.DatabaseService/CreateTable
```

✅ If successful, you should see proper responses, and a `user` table will be created in the database.


### 🧩 Database Configuration

The database connection URL is assumed to be:

```env
DATABASE_URL=mysql+pymysql://root:mysql@localhost:3306/dev_db
```

This is set in `config.py` and overridden by a `.env` file in the home directory.

---

## 🌐 Setting Up the FastAPI Server

### 1. Create and activate a virtual environment

```bash
py -3.10 -m venv venv
venv\Scripts\activate
```

### 2. Upgrade `pip`

```bash
python -m pip install --upgrade pip
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure protobuf files

a) Copy the generated protobuf files from the gRPC folder into `app/proto`.

b) Rename the files to:

- `database_pb2.py`
- `database_pb2_grpc.py`

c) Modify `database_pb2_grpc.py` to import as follows:

```python
from . import database_pb2 as database_service__pb2
```

### 5. Ensure all folders contain an `__init__.py` file

This includes:
- `app/`
- `app/proto/`
- Any submodules

### 6. Run the FastAPI server

```bash
uvicorn app.main:app --reload
```

You can now access the FastAPI server at:

- Home: http://localhost:8000  
- Swagger UI: http://localhost:8000/docs

---

## 📝 Creating a Record (via Swagger UI)

1. Go to the `/create_record/` endpoint.
2. Click **Try it out**.
3. Paste the following JSON into the request body:

```json
{
  "table_name": "user",
  "data": "{\"name\": \"akash\", \"email\": \"akash@email.com\"}"
}
```

4. Click **Execute**.

✅ If successful, the record will be added to the `user` table in your MySQL database.

> 🔔 Make sure the database and table already exist (created via gRPC earlier).
