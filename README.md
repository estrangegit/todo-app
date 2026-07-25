# Todo App

A full-stack Todo application built to explore modern backend and frontend development.

The project is composed of:

- **Backend:** FastAPI, SQLAlchemy, Alembic, PostgreSQL
- **Frontend:** Vue 3, TypeScript, Vite, Pinia, Vue Router
- **Infrastructure:** Docker & Docker Compose

---

# Features

## Backend

- REST API with FastAPI
- JWT Authentication
- Role-based authorization
- Todo ownership
- SQLAlchemy ORM
- Alembic database migrations
- PostgreSQL
- Pytest test suite

## Frontend

- Vue 3
- TypeScript
- Pinia state management
- Vue Router
- Vite
- ESLint
- Prettier

---

# Project Structure

```text
todo-app/
├── backend/
│   ├── app/
│   ├── tests/
│   ├── Dockerfile.dev
│   ├── requirements.txt
│   └── ...
│
├── frontend/
│   ├── src/
│   ├── public/
│   ├── Dockerfile.dev
│   ├── package.json
│   └── ...
│
├── docker-compose.dev.yml
├── docker-compose.test.yml
└── README.md
```

---

# Prerequisites

## Local development

- Python 3.13+
- Node.js 22+
- Docker Desktop

## Docker development

Only Docker Desktop is required.

---

# Development

Build and start the complete development environment.

```bash
docker compose -f docker-compose.dev.yml up --build
```

The following services will be started:

| Service | URL |
|----------|-----|
| Frontend | http://localhost:5173 |
| Backend API | http://localhost:8000 |
| Swagger UI | http://localhost:8000/docs |

Stop the environment:

```bash
docker compose -f docker-compose.dev.yml down
```

---

# Running Tests

Run the complete test environment.

```bash
docker compose -f docker-compose.test.yml up --build
```

Or execute the backend tests directly:

```bash
docker compose -f docker-compose.test.yml run --rm backend pytest
```

---

# Local Development

Running the application without Docker is still possible.

## Backend

```bash
cd backend

python -m venv .venv
source .venv/bin/activate
# Windows:
# .venv\Scripts\activate

pip install -r requirements.txt

uvicorn app.main:app --reload
```

## Frontend

```bash
cd frontend

npm install

npm run dev
```

---

# Database Migrations

Create a migration:

```bash
alembic revision --autogenerate -m "Description"
```

Apply migrations:

```bash
alembic upgrade head
```

Rollback:

```bash
alembic downgrade -1
```

---

# Code Quality

## Backend

Run the tests:

```bash
pytest
```

## Frontend

Lint:

```bash
npm run lint
```

Format:

```bash
npm run format
```

---

# Docker

The project currently provides two Docker Compose configurations.

| File | Purpose |
|------|---------|
| docker-compose.dev.yml | Development environment |
| docker-compose.test.yml | Test environment |

A production configuration (`docker-compose.prod.yml`) will be added later.

---

# Notes

The frontend runs inside Docker using Vite.

On Docker Desktop (Windows/macOS), Vite uses polling for file watching to enable Hot Module Replacement (HMR).

---

# Roadmap

- Authentication UI
- Todo CRUD interface
- User management
- Production deployment
- CI/CD improvements
