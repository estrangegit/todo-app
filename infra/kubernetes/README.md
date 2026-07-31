# Kubernetes

## Deploy the application

### 1. Push Docker images to GHCR

Backend:

```bash
docker tag todo-app-backend:latest ghcr.io/<github-user>/todo-app-backend:latest
docker push ghcr.io/<github-user>/todo-app-backend:latest
```

Frontend:

```bash
docker tag todo-app-frontend:latest ghcr.io/<github-user>/todo-app-frontend:latest
docker push ghcr.io/<github-user>/todo-app-frontend:latest
```

---

### 2. Delete the existing environment

```bash
kubectl delete namespace todo-app
```

---

### 3. Create the namespace

```bash
kubectl apply -f infra/kubernetes/namespace.yaml
```

---

### 4. Deploy PostgreSQL

```bash
kubectl -n todo-app apply -f infra/kubernetes/postgres/
```

Verify that the pod is running:

```bash
kubectl get pods -n todo-app
```

---

### 5. Deploy the backend

```bash
kubectl -n todo-app apply -f infra/kubernetes/backend/
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

### 6. Deploy the frontend

```bash
kubectl -n todo-app apply -f infra/kubernetes/frontend/
```

Verify the deployment:

```bash
kubectl get pods -n todo-app
```

---

## Access the services

### Backend

```bash
kubectl port-forward service/backend 8000:8000 -n todo-app
```

The API is available at:

```text
http://localhost:8000
```

OpenAPI documentation:

```text
http://localhost:8000/docs
```

### PostgreSQL

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

### Frontend

```bash
kubectl port-forward service/frontend 80:80 -n todo-app
```

The application is available at:

```text
http://localhost:80
```

## Database migrations and seed data

### 1. Forward the PostgreSQL service

```bash
kubectl port-forward service/postgres 5432:5432 -n todo-app
```

Keep this terminal open while running the following commands.

---

### 2. Activate the Python virtual environment

```bash
cd backend

# Linux / macOS
source .venv/bin/activate

# Windows (PowerShell)
.venv\Scripts\Activate.ps1
```

---

### 3. Configure the local environment

Use the development environment:

```bash
# Linux / macOS
export APP_ENV=dev

# Windows (PowerShell)
$env:APP_ENV="dev"
```

Update the database connection so that it points to the forwarded PostgreSQL service.

Either edit `.env.dev`:

```text
DATABASE_URL=postgresql+psycopg://todo_user:123456@localhost:5432/todo_db
```

or override it from the command line:

```bash
# Linux / macOS
export DATABASE_URL=postgresql+psycopg://todo_user:123456@localhost:5432/todo_db

# Windows (PowerShell)
$env:DATABASE_URL="postgresql+psycopg://todo_user:123456@localhost:5432/todo_db"
```

---

### 4. Run Alembic migrations

```bash
alembic upgrade head
```

---

### 5. Load the seed data

```bash
python -m app.db.seed.seed
```
