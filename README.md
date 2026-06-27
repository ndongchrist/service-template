# service-template

Cookiecutter that generates a structurally-identical DRF microservice for the
e-commerce platform. One mental model for every service — the cure for polyrepo
drift.

## What it generates

- **DRF app** with `config/` project, `/health/` (liveness) + `/health/ready/`
  (readiness, DB-checked), correlation-id + trusted-user (`X-User-Id`) middleware.
- **Transactional outbox** baked in: `OutboxEvent` model, `emit_event()`, and a
  `relay_outbox` management command that runs as its own Deployment.
- **Multi-stage Dockerfile** (uv build stage → slim runtime, non-root uid 10001,
  read-only-rootfs-ready, tini as PID 1).
- **Helm chart** (`chart/`): Deployment, Service (ClusterIP), ConfigMap, HPA,
  ServiceMonitor, three probes, **mandatory** resource requests/limits, a
  pre-install/upgrade migration Job, and an opt-in outbox-relay Deployment.
- **CI** (`.github/workflows/ci.yml`): ruff → mypy → pytest → trivy → build/push
  image (git SHA) → bump that tag in the `infra` repo (GitOps; never deploys).

## Variables (`cookiecutter.json`)

| Var | Example | Notes |
|---|---|---|
| `service_name` | `catalog` | drives everything below |
| `service_slug` | `catalog-service` | repo + chart name (auto) |
| `app_name` | `catalog` | Django app package (auto) |
| `python_version` | `3.12` | |
| `django_version` | `5.1.4` | |
| `http_port` | `8000` | container port |

## Generate a service

```bash
# Render into a temp dir, then sync into the already-cloned service repo
cookiecutter /path/to/service-template --no-input service_name=catalog -o /tmp/gen
rsync -a --exclude='.git' /tmp/gen/catalog-service/ /path/to/catalog-service/
```

(The platform build does this for all five services; see the parent workspace.)
