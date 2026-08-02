# Todo App

## 1. Prerequisites

The following tools must be installed:

- Docker Desktop
- kubectl
- Helm

### Kubernetes cluster

A Kubernetes cluster must be running:

```powershell
kubectl cluster-info
kubectl get nodes
```

### NGINX Ingress Controller

Install the NGINX Ingress Controller for kind:

```powershell
kubectl apply `
    -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/kind/deploy.yaml
```

Check the controller:

```powershell
kubectl get pods -n ingress-nginx
```

---

## 2. Architecture

```text
                         ┌─────────────┐
                         │   Browser   │
                         └──────┬──────┘
                                │
                                ▼
                         ┌─────────────┐
                         │   Ingress   │
                         └──────┬──────┘
                                │
                    ┌───────────┴───────────┐
                    │                       │
                    ▼                       ▼
             ┌─────────────┐         ┌─────────────┐
             │  Frontend   │         │   Backend   │
             └─────────────┘         └──────┬──────┘
                                            │
                                            ▼
                                     ┌─────────────┐
                                     │ PostgreSQL  │
                                     └─────────────┘


                Application logs
                       │
                       ▼
                    Alloy
                       │
                       ▼
                     Loki
                       │
                       ▼
                    Grafana
```

---

## 3. Application deployment

Create the application namespace:

```powershell
kubectl apply `
    -f .\infra\kubernetes\todo-app\namespace.yaml
```

### PostgreSQL

```powershell
helm upgrade --install postgres `
    .\infra\helm\todo-app\postgres `
    --namespace todo-app `
    --wait `
    --timeout 5m
```

### Backend

Replace `<GIT_COMMIT_SHA>` with the Docker image tag to deploy:

```powershell
helm upgrade --install backend `
    .\infra\helm\todo-app\backend `
    --namespace todo-app `
    --set-string image.tag="<GIT_COMMIT_SHA>" `
    --wait `
    --timeout 5m
```

### Frontend

```powershell
helm upgrade --install frontend `
    .\infra\helm\todo-app\frontend `
    --namespace todo-app `
    --set-string image.tag="<GIT_COMMIT_SHA>" `
    --wait `
    --timeout 5m
```

### Ingress

```powershell
helm upgrade --install ingress `
    .\infra\helm\todo-app\ingress `
    --namespace todo-app `
    --wait `
    --timeout 5m
```

### Check deployment

```powershell
helm list -n todo-app
kubectl get pods -n todo-app
kubectl get ingress -n todo-app
```

---

## 4. Database migrations

Apply all Alembic migrations from the Kubernetes backend:

```powershell
kubectl exec deployment/backend `
    -n todo-app -- `
    alembic upgrade head
```

Check the current database revision:

```powershell
kubectl exec deployment/backend `
    -n todo-app -- `
    alembic current
```

Load development seed data if required:

```powershell
kubectl exec deployment/backend `
    -n todo-app -- `
    python -m app.db.seed.seed
```

---

## 5. Observability deployment

Deploy the observability namespace:

```powershell
kubectl apply `
    -f .\infra\kubernetes\observability\namespace.yaml
```

Deploy Loki:

```powershell
kubectl apply `
    -f .\infra\kubernetes\observability\loki/
```

Deploy Alloy:

```powershell
kubectl apply `
    -f .\infra\kubernetes\observability\alloy/
```

Deploy Grafana:

```powershell
kubectl apply `
    -f .\infra\kubernetes\observability\grafana/
```

### Check deployment

```powershell
kubectl get pods -n observability
```

Check Alloy logs:

```powershell
kubectl logs `
    -n observability `
    -l app=alloy `
    --prefix
```

---

## Future improvements

The next main improvement is to better integrate **Alembic migrations into the CD pipeline**.

Migrations should be handled as a dedicated deployment step, independently from seed data, with explicit failure and rollback handling.

A dedicated Kubernetes `Job` could eventually execute the migrations before the new backend version is deployed.

A Helm rollback does not roll back the PostgreSQL schema, so application and database rollback strategies must be considered together.
