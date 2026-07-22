# Todo API

A RESTful Todo API built with **FastAPI**, **SQLAlchemy**, and **PostgreSQL**.

This project was created as a learning exercise to explore the FastAPI ecosystem while following practices commonly used in professional backend applications, including layered architecture, database migrations, integration testing, and continuous integration with GitLab CI.

## 🚀 Tech Stack

* Python 3.14
* FastAPI
* SQLAlchemy
* PostgreSQL
* Alembic
* Pytest
* Docker Compose
* GitLab CI

---

## 📋 Prerequisites

Before running the project, make sure you have installed:

* Python 3.14
* Docker Desktop
* Git

---

## ⚙️ Installation

### Clone the repository

```powershell
git clone <repository-url>
cd todo-api
```
### Create a virtual environment

```powershell
python -m venv .venv
```

### Activate the virtual environment

```powershell
.\.venv\Scripts\Activate.ps1
```

### Install dependencies

```powershell
pip install -r requirements.txt
```
---

## 💻 Development workflow

The following commands are typically executed at the beginning of a development session.

### 1. Activate the virtual environment

```powershell
.\.venv\Scripts\Activate.ps1
```

### 2. Select the development environment

```powershell
$env:APP_ENV = "dev"
```

### 3. Start PostgreSQL

```powershell
docker compose up -d
```

### 4. Apply database migrations

```powershell
alembic upgrade head
```

### 5. Run the application

```powershell
uvicorn app.main:app --reload
```

The API will be available at:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## 🧪 Testing workflow

Switch to the test environment before running the test suite.

```powershell
$env:APP_ENV = "test"

pytest -v
```

---

## 🌍 Environment configuration

Select the environment before running the application.

### Development

```powershell
$env:APP_ENV = "dev"
```

### Testing

```powershell
$env:APP_ENV = "test"
```

### Production

```powershell
$env:APP_ENV = "prod"
```

Verify the current value:

```powershell
echo $env:APP_ENV
```

> **Note**
>
> The environment variable is only available for the current PowerShell session.

---

## 🐘 Database

Start PostgreSQL:

```powershell
docker compose up -d
```

Apply database migrations:

```powershell
alembic upgrade head
```

---

## ▶️ Run the application

```powershell
uvicorn app.main:app --reload
```

Once the application is running:

* Swagger UI: http://localhost:8000/docs
* ReDoc: http://localhost:8000/redoc

---

## 🧪 Run the tests

Before running the test suite, select the testing environment:

```powershell
$env:APP_ENV = "test"
pytest -v
```

---

## 🛠️ Useful commands

### Create a new migration

```powershell
alembic revision --autogenerate -m "description"
```

### Apply all migrations

```powershell
alembic upgrade head
```

### Roll back the last migration

```powershell
alembic downgrade -1
```

### Show the current migration

```powershell
alembic current
```

### Display migration history

```powershell
alembic history
```

---

## 📁 Project structure

```text
app/
├── api/
├── core/
├── db/
├── exceptions/
├── models/
├── schemas/
├── services/
└── main.py

tests/
alembic/
```

---

## 🔄 Continuous Integration

Every push triggers a GitLab CI pipeline that:

1. Starts a PostgreSQL database.
2. Applies the latest Alembic migrations.
3. Runs the integration test suite using Pytest.

---

## 🎯 Learning goals

The purpose of this project is to gain hands-on experience with the FastAPI ecosystem by progressively implementing features commonly found in production-ready REST APIs.

Throughout the project, particular attention is given to:

* Clean project architecture
* Dependency Injection with FastAPI
* SQLAlchemy ORM
* Database versioning with Alembic
* Integration testing with Pytest
* Continuous Integration with GitLab CI
* REST API best practices
