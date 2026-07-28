# Todo App

A full-stack Todo application built to explore modern backend and frontend development using a production-like architecture.

The application is developed with FastAPI and Vue 3 and runs in Docker using Nginx as a reverse proxy.

---

# Technology Stack

## Backend

- FastAPI
- SQLAlchemy
- Alembic
- PostgreSQL
- JWT Authentication
- Pytest

## Frontend

- Vue 3
- TypeScript
- Vite
- Vue Router
- Pinia
- PrimeVue
- Zod
- Axios

## Infrastructure

- Docker
- Docker Compose
- Nginx

---

# Architecture

```text
                 Browser
                    │
                    ▼
                 Nginx (80)
                 │       │
                 │       └────────► FastAPI (/api)
                 │
                 └───────────────► Vite
                                       │
                                       ▼
                                  PostgreSQL
```

The frontend communicates exclusively with `/api`.

During development, Nginx proxies:

- `/` → Vite development server
- `/api` → FastAPI

This provides a production-like architecture while keeping Hot Module Replacement (HMR) enabled.

---

# Features

## Backend

- REST API
- JWT authentication
- Role-based authorization
- Todo ownership
- SQLAlchemy ORM
- Alembic migrations
- PostgreSQL
- Dockerized development
- Development seed

## Frontend

- Vue 3
- TypeScript
- Vue Router
- Pinia
- PrimeVue Forms
- Zod validation
- Axios API client

---

# Project Structure

```text
todo-app/

├── backend/
│   ├── app/
│   │   ├── db/
│   │   │   └── seed/
│   │   ├── models/
│   │   ├── routers/
│   │   ├── services/
│   │   └── ...
│   ├── tests/
│   └── ...
│
├── frontend/
│   ├── src/
│   └── ...
│
├── nginx/
│   ├── nginx.dev.conf
│   └── nginx.prod.conf
│
├── docker-compose.dev.yml
├── docker-compose.test.yml
└── README.md
```

---

# Prerequisites

## Docker development

- Docker Desktop

## Local development

- Python 3.13+
- Node.js 22+

---

# Development

Build and start the complete development environment.

```bash
docker compose -f docker-compose.dev.yml up --build
```

The following services will be available.

| Service | URL |
|----------|-----|
| Application | http://localhost |
| API | http://localhost/api |
| Swagger UI | http://localhost/docs |

Stop the environment.

```bash
docker compose -f docker-compose.dev.yml down
```

---

# Development Seed

The backend provides a development seed.

The seed:

- clears the development data
- creates demo users
- creates fixed tasks
- generates reproducible random tasks using Faker

## Demo users

| Username | Password | Role |
|----------|----------|------|
| admin | admin123 | ADMIN |
| alice | alice123 | USER |
| bob | bob123 | USER |

Start the database.

```bash
docker compose -f docker-compose.dev.yml up db -d
```

Apply database migrations.

```bash
docker compose -f docker-compose.dev.yml run --rm backend alembic upgrade head
```

Load the development seed.

```bash
docker compose -f docker-compose.dev.yml run --rm backend python -m app.db.seed.seed
```

---

# Running Tests

Run the complete test environment.

```bash
docker compose -f docker-compose.test.yml up --build
```

Or execute only the backend tests.

```bash
docker compose -f docker-compose.test.yml run --rm backend pytest
```

---

# Local Development

Running the application without Docker is still possible.

This is especially useful when using an IDE debugger.

## Backend

```bash
cd backend

python -m venv .venv

# Linux/macOS
source .venv/bin/activate

# Windows
.venv\Scripts\activate

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

Create a migration.

```bash
alembic revision --autogenerate -m "Description"
```

Apply migrations.

```bash
alembic upgrade head
```

Rollback.

```bash
alembic downgrade -1
```

---

# Code Quality

## Backend

Run the tests.

```bash
pytest
```

## Frontend

Lint.

```bash
npm run lint
```

Format.

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

A production configuration will be added later.

---

# Notes

- The frontend runs behind Nginx.
- Vite Hot Module Replacement (HMR) is proxied through Nginx using WebSockets.
- Development data can be regenerated at any time using the seed script.

---

# Roadmap

- Authentication UI
- Todo CRUD interface
- User management
- Production deployment
- CI/CD improvements
