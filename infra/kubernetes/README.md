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
