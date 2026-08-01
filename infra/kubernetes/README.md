# Kubernetes

This directory contains the Kubernetes configuration used to deploy the Todo application and its observability stack.

The application consists of:

- PostgreSQL
- FastAPI backend
- Frontend served by NGINX
- NGINX Ingress Controller

The observability stack consists of:

- Grafana Alloy
- Loki
- Grafana

## Architecture

```text
                              Kubernetes cluster

                                 ┌─────────────┐
                                 │    NGINX    │
todo.local ────────────────────► │   Ingress   │
                                 │ Controller  │
                                 └──────┬──────┘
                                        │
                              ┌─────────┴─────────┐
                              │                   │
                              ▼                   ▼
                          Frontend             Backend
                                                  │
                                                  ▼
                                              PostgreSQL


                              Observability

                      Worker 1              Worker 2
                         │                     │
                       Alloy                 Alloy
                         │                     │
                         └──────────┬──────────┘
                                    │
                                    ▼
                                   Loki
                                    ▲
                                    │
                                 Grafana
                                    ▲
                                    │
                         grafana.todo.local
```

All application resources are deployed in the `todo-app` namespace.

Observability resources are deployed in the `observability` namespace.

---

## Prerequisites

Before deploying the application, ensure that:

- Docker Desktop is installed.
- A Kubernetes cluster is running.
- `kubectl` is configured to access the cluster.
- The latest backend and frontend images have been published to GHCR.
- The NGINX Ingress Controller is installed.
- The self-hosted GitHub Actions runner can access the Kubernetes cluster.

Verify the cluster:

```powershell
kubectl cluster-info
kubectl get nodes
```

### Install the NGINX Ingress Controller

For a Kind cluster:

```powershell
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/kind/deploy.yaml
```

Verify the controller:

```powershell
kubectl get pods -n ingress-nginx
```

---

# Local DNS

Add the following entries to the local `hosts` file:

```text
127.0.0.1 todo.local
127.0.0.1 grafana.todo.local
```

On Windows, the file is located at:

```text
C:\Windows\System32\drivers\etc\hosts
```

The application is available at:

```text
http://todo.local
```

Grafana is available at:

```text
http://grafana.todo.local
```

---

# Container images

Backend and frontend images are stored in GitHub Container Registry.

Images are published using the GitHub Actions workflow:

```text
publish-images.yml
```

The deployment workflow accepts an image tag through the `imageTag` parameter.

This allows a specific application version to be deployed instead of relying exclusively on the `latest` tag.

---

# Continuous Deployment

The application and observability stack can be deployed using:

```text
deploy-kubernetes.yml
```

The workflow runs on a self-hosted GitHub Actions runner with access to the Kubernetes cluster.

## Workflow parameters

### `imageTag`

Docker image tag to deploy.

Example:

```text
abc1234
```

The workflow deploys:

```text
ghcr.io/<owner>/todo-app-backend:abc1234
ghcr.io/<owner>/todo-app-frontend:abc1234
```

### `resetApplication`

When enabled, the workflow deletes the complete `todo-app` namespace before redeploying the application.

```text
resetApplication = true
        │
        ▼
delete namespace todo-app
        │
        ▼
recreate application resources
```

Use this option when a completely clean application environment is required.

### `resetObservability`

When enabled, the workflow deletes the complete `observability` namespace before redeploying Loki, Alloy, and Grafana.

```text
resetObservability = true
        │
        ▼
delete namespace observability
        │
        ▼
recreate observability stack
```

This is useful during development when testing the observability infrastructure from a clean state.

Be aware that deleting this namespace may also delete observability data when persistent storage is attached to resources in the namespace.

### `seed`

When enabled, database migrations and sample data are applied from the backend container.

The workflow executes:

```powershell
kubectl exec deployment/backend `
    -n todo-app -- `
    alembic upgrade head
```

followed by:

```powershell
kubectl exec deployment/backend `
    -n todo-app -- `
    python -m app.db.seed.seed
```

---

# Application deployment

Application resources are stored under:

```text
infra/kubernetes/todo-app/
```

The main resources are:

```text
todo-app/
├── namespace.yaml
├── postgres/
├── backend/
├── frontend/
└── ingress/
```

## PostgreSQL

Deploy PostgreSQL:

```powershell
kubectl apply -n todo-app -f infra/kubernetes/todo-app/postgres/
```

Verify the StatefulSet:

```powershell
kubectl rollout status statefulset/postgres -n todo-app
```

Inspect the pod:

```powershell
kubectl get pods -n todo-app
```

## Backend

Deploy the backend:

```powershell
kubectl apply -n todo-app -f infra/kubernetes/todo-app/backend/
```

Inspect the deployment:

```powershell
kubectl get deployment backend -n todo-app
```

Inspect the logs:

```powershell
kubectl logs deployment/backend -n todo-app
```

## Frontend

Deploy the frontend:

```powershell
kubectl apply -n todo-app -f infra/kubernetes/todo-app/frontend/
```

Inspect the deployment:

```powershell
kubectl get deployment frontend -n todo-app
```

## Ingress

Deploy the application Ingress:

```powershell
kubectl apply -n todo-app -f infra/kubernetes/todo-app/ingress/
```

Verify the Ingress:

```powershell
kubectl get ingress -n todo-app
```

The application Ingress routes:

```text
/      → frontend
/api   → backend
```

---

# Kubernetes health checks

The application uses Kubernetes probes to determine whether containers are healthy and ready to receive traffic.

## Backend

The backend exposes two health endpoints:

```text
GET /health/live
GET /health/ready
```

### Liveness probe

The liveness probe determines whether the backend process is still functioning.

If it repeatedly fails, Kubernetes restarts the container.

### Readiness probe

The readiness probe determines whether the backend can receive application traffic.

The readiness endpoint also verifies database availability.

When readiness fails, Kubernetes removes the Pod from the Service endpoints until it becomes ready again.

## Frontend

The frontend probes perform HTTP requests against the NGINX server.

They verify that the frontend container is running and able to serve HTTP traffic.

## PostgreSQL

PostgreSQL health checks use:

```text
pg_isready
```

to determine whether the database server is accepting connections.

---

# Observability

Observability resources are stored under:

```text
infra/kubernetes/observability/
```

The structure is:

```text
observability/
├── namespace.yaml
├── loki/
├── alloy/
└── grafana/
```

The observability pipeline is:

```text
Application containers
        │
        │ stdout / stderr
        ▼
     Kubernetes
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

## Grafana Alloy

Alloy is responsible for discovering Kubernetes Pods and collecting their container logs.

Alloy is deployed as a Kubernetes `DaemonSet`.

This means one Alloy Pod runs on each eligible worker node.

For example:

```text
Worker 1                    Worker 2
────────                    ────────
Backend                     Frontend
                            PostgreSQL

Alloy                       Alloy
  │                           │
  └─────────────┬─────────────┘
                ▼
               Loki
```

The control plane does not run Alloy when it has the following taint:

```text
node-role.kubernetes.io/control-plane:NoSchedule
```

Alloy only discovers Pods from the `todo-app` namespace.

Its Kubernetes discovery configuration is restricted using:

```alloy
namespaces {
  names = ["todo-app"]
}
```

Each Alloy instance also restricts discovery to its own node.

This prevents multiple Alloy instances from collecting the same Pod logs.

---

## Loki

Loki receives and stores the logs collected by Alloy.

Loki is only exposed internally through a Kubernetes `ClusterIP` Service.

Alloy sends logs to:

```text
http://loki:3100
```

The Loki readiness endpoint is:

```text
/ready
```

It is used by the Kubernetes readiness probe to determine when Loki is ready to receive traffic.

Loki currently runs in single-tenant mode:

```yaml
auth_enabled: false
```

---

## Grafana

Grafana provides the user interface used to explore logs stored in Loki.

Loki is automatically provisioned as a Grafana datasource using a Kubernetes ConfigMap.

Grafana connects internally to:

```text
http://loki:3100
```

Grafana is exposed through the NGINX Ingress Controller at:

```text
http://grafana.todo.local
```

---

# Query logs

Open Grafana and navigate to **Explore**.

Select the Loki datasource.

## All application logs

```logql
{namespace="todo-app"}
```

## Backend logs

```logql
{namespace="todo-app", app="backend"}
```

## Frontend logs

```logql
{namespace="todo-app", app="frontend"}
```

## PostgreSQL logs

```logql
{namespace="todo-app", app="postgres"}
```

## Hide backend health probes

Backend probes generate regular HTTP access logs.

They can be excluded from a query using:

```logql
{namespace="todo-app", app="backend"}
  != "/health/ready"
  != "/health/live"
```

Probe logs are currently retained by Loki because they can still be useful when diagnosing Kubernetes health-check problems.

---

# Manual deployment

The GitHub Actions workflow is the recommended deployment method, but the complete environment can also be deployed manually.

## Reset the application

```powershell
kubectl delete namespace todo-app --ignore-not-found=true
```

## Reset observability

```powershell
kubectl delete namespace observability --ignore-not-found=true
```

## Deploy the application

```powershell
kubectl apply -f infra/kubernetes/todo-app/namespace.yaml

kubectl apply -n todo-app -f infra/kubernetes/todo-app/postgres/
kubectl apply -n todo-app -f infra/kubernetes/todo-app/backend/
kubectl apply -n todo-app -f infra/kubernetes/todo-app/frontend/
kubectl apply -n todo-app -f infra/kubernetes/todo-app/ingress/
```

Wait for PostgreSQL:

```powershell
kubectl rollout status statefulset/postgres `
    -n todo-app `
    --timeout=300s
```

Wait for the application:

```powershell
kubectl rollout status deployment/backend `
    -n todo-app `
    --timeout=300s

kubectl rollout status deployment/frontend `
    -n todo-app `
    --timeout=300s
```

## Deploy observability

```powershell
kubectl apply -f infra/kubernetes/observability/namespace.yaml

kubectl apply -f infra/kubernetes/observability/loki/
kubectl apply -f infra/kubernetes/observability/alloy/
kubectl apply -f infra/kubernetes/observability/grafana/
```

Wait for the observability stack:

```powershell
kubectl rollout status deployment/loki `
    -n observability `
    --timeout=300s

kubectl rollout status daemonset/alloy `
    -n observability `
    --timeout=300s

kubectl rollout status deployment/grafana `
    -n observability `
    --timeout=300s
```

---

# Cluster status

## Application

```powershell
kubectl get pods -n todo-app -o wide
kubectl get svc -n todo-app
kubectl get ingress -n todo-app
```

## Observability

```powershell
kubectl get pods -n observability -o wide
kubectl get svc -n observability
kubectl get ingress -n observability
kubectl get daemonsets -n observability
```

---

# Access individual services

Services can still be accessed directly using `kubectl port-forward` when debugging.

## Backend API

```powershell
kubectl port-forward service/backend 8000:8000 -n todo-app
```

OpenAPI documentation:

```text
http://localhost:8000/docs
```

## PostgreSQL

```powershell
kubectl port-forward service/postgres 5432:5432 -n todo-app
```

## Loki

```powershell
kubectl port-forward service/loki 3100:3100 -n observability
```

Check Loki readiness:

```powershell
Invoke-WebRequest http://localhost:3100/ready
```

## Grafana

Grafana normally does not require port forwarding because it is exposed through the Ingress.

For debugging, direct access is still possible:

```powershell
kubectl port-forward service/grafana 3000:3000 -n observability
```

Then open:

```text
http://localhost:3000
```

---

# Database migrations and seed data

Database migrations and seed data can be applied either automatically through the deployment workflow or manually from the Windows development environment.

## Database connection

PostgreSQL is only exposed inside the Kubernetes cluster.

To access it from Windows, create a port-forward:

```powershell
kubectl port-forward service/postgres 5432:5432 -n todo-app
```

Keep this terminal open while running the following commands.

The local connection parameters are:

```text
Host: localhost
Port: 5432
Database: todo
Username: <database-user>
Password: <database-password>
```

The actual credentials are stored in Kubernetes Secrets and should not be committed to the repository.

---

## Configure the database environment variables

Open a second PowerShell terminal and configure the environment variables required by the backend:

```powershell
$env:POSTGRES_HOST="localhost"
$env:POSTGRES_PORT="5432"
$env:POSTGRES_DB="todo"
$env:POSTGRES_USER="<database-user>"
$env:POSTGRES_PASSWORD="<database-password>"
```

You can verify the values with:

```powershell
Get-ChildItem Env:POSTGRES_*
```

These environment variables only apply to the current PowerShell session.

---

## Apply database migrations

From the backend project directory, apply all pending Alembic migrations:

```powershell
alembic upgrade head
```

Check the current migration:

```powershell
alembic current
```

Display the migration history:

```powershell
alembic history
```

---

## Load seed data

Once the database schema is up to date, load the sample data:

```powershell
python -m app.db.seed.seed
```

---

## Apply migrations from Kubernetes

Migrations can also be executed directly inside the running backend container:

```powershell
kubectl exec deployment/backend -n todo-app -- alembic upgrade head
```

Load the seed data:

```powershell
kubectl exec deployment/backend -n todo-app -- python -m app.db.seed.seed
```

This is the approach used by the Kubernetes deployment workflow when the `seed` option is enabled.

---

## Open a PostgreSQL shell

A PostgreSQL shell can be opened directly inside the database container:

```powershell
kubectl exec -it postgres-0 -n todo-app -- psql -U <database-user> -d todo
```

Once connected, list the tables:

```text
\dt
```

Check the Alembic revision:

```sql
SELECT * FROM alembic_version;
```

Exit PostgreSQL with:

```text
\q
```

---

## Stop the port-forward

When the local database operations are complete, return to the terminal running:

```powershell
kubectl port-forward service/postgres 5432:5432 -n todo-app
```

and press:

```text
Ctrl+C
```

to stop the port-forward.

---

# Troubleshooting

## Inspect Pods

```powershell
kubectl get pods -n todo-app -o wide
kubectl get pods -n observability -o wide
```

## Describe a Pod

```powershell
kubectl describe pod <pod-name> -n <namespace>
```

## Backend logs

```powershell
kubectl logs deployment/backend -n todo-app
```

## Alloy logs

Because Alloy runs as a DaemonSet, use the label selector to retrieve logs from all Alloy Pods:

```powershell
kubectl logs `
    -n observability `
    -l app=alloy `
    --prefix
```

## Loki logs

```powershell
kubectl logs deployment/loki -n observability
```

## Grafana logs

```powershell
kubectl logs deployment/grafana -n observability
```

## Check rollouts

```powershell
kubectl rollout status deployment/backend -n todo-app
kubectl rollout status deployment/frontend -n todo-app

kubectl rollout status deployment/loki -n observability
kubectl rollout status daemonset/alloy -n observability
kubectl rollout status deployment/grafana -n observability
```
