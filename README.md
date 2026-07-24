# Todo API

A RESTful Todo API built with **FastAPI**, **SQLAlchemy**, and **PostgreSQL**.

This project was created as a learning exercise to explore the FastAPI ecosystem while following practices commonly used in production backend applications, including:

- Layered architecture
- JWT authentication
- Role-based authorization
- Database migrations with Alembic
- Integration testing
- Docker-based development
- GitLab CI

---

# 🚀 Tech Stack

- Python 3.14
- FastAPI
- SQLAlchemy
- PostgreSQL
- Alembic
- Pytest
- Docker & Docker Compose
- GitLab CI

---

# 📋 Prerequisites

Install the following tools:

- Git
- Docker Desktop
- Python 3.14 (required only for local debugging with PyCharm Community)

---

# ⚙️ Installation

Clone the repository:

```bash
git clone <repository-url>
cd todo-api
```

Create a local virtual environment (optional but recommended for PyCharm Community):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

---

# 💻 Development

This project supports two development workflows.

## Option 1 — Docker (recommended)

Start the application:

```powershell
docker compose up --build
```

The API is available at:

- http://localhost:8000/docs
- http://localhost:8000/redoc

Stop the application:

```powershell
docker compose down
```

Rebuild the image after changing dependencies:

```powershell
docker compose up --build
```

---

## Option 2 — Local debugging

PyCharm Community does not support Docker interpreters.

For debugging, a local virtual environment is kept while PostgreSQL still runs inside Docker.

Activate the virtual environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

Select the environment:

```powershell
$env:APP_ENV="dev"
```

Start PostgreSQL:

```powershell
docker compose up db -d
```

Apply database migrations:

```powershell
alembic upgrade head
```

Run the application:

```powershell
uvicorn app.main:app --reload
```

---

# 🧪 Running the tests

Run the complete integration test suite inside Docker:

```powershell
docker compose -f docker-compose.test.yml run --rm backend
```

Note: The PostgreSQL container remains running after the test execution. To stop and remove all test containers, run:

```powershell
docker compose -f docker-compose.test.yml down
```

This command automatically:

- starts PostgreSQL
- applies Alembic migrations
- runs the tests
- removes the test container

---

# 🛠️ Useful commands

Open a shell inside the backend container:

```powershell
docker compose exec backend sh
```

Apply migrations:

```powershell
docker compose exec backend alembic upgrade head
```

Create a migration:

```powershell
docker compose exec backend alembic revision --autogenerate -m "description"
```

Rollback the last migration:

```powershell
docker compose exec backend alembic downgrade -1
```

Show the current revision:

```powershell
docker compose exec backend alembic current
```

Migration history:

```powershell
docker compose exec backend alembic history
```

---

# 📁 Project structure

```text
app/
├── api/
├── core/
├── db/
├── domain/
├── enums/
├── exceptions/
├── models/
├── schemas/
├── services/
├── dependencies.py
├── security.py
└── main.py

tests/
alembic/
scripts/
docker-compose.yml
docker-compose.test.yml
```

---

# 🔄 Continuous Integration

Every push triggers a GitLab CI pipeline that:

1. Builds the application image
2. Starts PostgreSQL
3. Applies the latest Alembic migrations
4. Runs the integration test suite

---

# 📌 Notes

- The project follows a **Docker-first** workflow.
- The local virtual environment exists only because **PyCharm Community** cannot use Docker interpreters.
- The CI pipeline and production environment both run entirely inside Docker.
