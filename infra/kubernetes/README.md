# Kubernetes

## Prerequisites

Before deploying the application, ensure that:

- Docker Desktop is installed with Kubernetes enabled.
- A Kubernetes cluster has been created.
- The latest backend and frontend images have been published to GHCR.
- The NGINX Ingress Controller is installed.

Install the Ingress Controller:

```bash
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/kind/deploy.yaml
```

Add the following entry to your hosts file:

```text
127.0.0.1 todo.local
```

---

## Publish Docker images

Publish the latest images to GitHub Container Registry using the GitHub Actions workflow:

```
publish-images.yml
```

Wait until the workflow completes successfully before deploying.

---

# Deploy the application

## 1. Delete the existing environment

```bash
kubectl delete namespace todo-app
```

---

## 2. Create the namespace

```bash
kubectl apply -f infra/kubernetes/namespace.yaml
```

---

## 3. Deploy PostgreSQL

```bash
kubectl apply -n todo-app -f infra/kubernetes/postgres/
```

Verify that the pod is running:

```bash
kubectl get pods -n todo-app
```

---

## 4. Deploy the backend

```bash
kubectl apply -n todo-app -f infra/kubernetes/backend/
```

Verify the deployment:

```bash
kubectl get pods -n todo-app
```

If something goes wrong:

```bash
kubectl logs deployment/backend -n todo-app
kubectl describe pod <pod-name> -n todo-app
```

---

## 5. Deploy the frontend

```bash
kubectl apply -n todo-app -f infra/kubernetes/frontend/
```

Verify the deployment:

```bash
kubectl get pods -n todo-app
```

---

## 6. Deploy the Ingress

```bash
kubectl apply -n todo-app -f infra/kubernetes/ingress/
```

Verify the Ingress:

```bash
kubectl get ingress -n todo-app
```

---

# Access the application

Open:

```text
http://todo.local
```

The Ingress routes:

- `/` → frontend
- `/api` → backend

---

# Access individual services

## Backend API

For direct access to the API:

```bash
kubectl port-forward service/backend 8000:8000 -n todo-app
```

OpenAPI documentation:

```text
http://localhost:8000/docs
```

---

## PostgreSQL

```bash
kubectl port-forward service/postgres 5432:5432 -n todo-app
```

Connection details:

```text
Host: localhost
Port: 5432
Database: todo_db
Username: todo_user
Password: 123456
```

---

# Database migrations and seed data

## 1. Forward the PostgreSQL service

```bash
kubectl port-forward service/postgres 5432:5432 -n todo-app
```

Keep this terminal open.

---

## 2. Activate the Python virtual environment

```bash
# Linux / macOS
source .venv/bin/activate

# Windows (PowerShell)
.venv\Scripts\Activate.ps1
```

---

## 3. Configure the local environment

Use the development environment:

```bash
# Linux / macOS
export APP_ENV=dev

# Windows (PowerShell)
$env:APP_ENV="dev"
```

Override the database connection:

```bash
# Linux / macOS
export DATABASE_URL=postgresql+psycopg://todo_user:123456@localhost:5432/todo_db

# Windows (PowerShell)
$env:DATABASE_URL="postgresql+psycopg://todo_user:123456@localhost:5432/todo_db"
```

---

## 4. Apply database migrations

```bash
cd backend
alembic upgrade head
```

---

## 5. Load seed data

```bash
python -m app.db.seed.seed
```
