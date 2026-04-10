# Docker Deployment Guide

This guide covers local and server-style deployment using Docker Compose.

## 1. Prerequisites

- Docker Desktop (Windows/macOS) or Docker Engine + Compose plugin (Linux)
- Ports available:
  - `8080` (frontend)
  - `8000` (backend API/docs)
  - `5432` (PostgreSQL)
  - `6379` (Redis)

## 2. Prepare Environment

1. From project root, copy env file:
   ```bash
   cp .env.example .env
   ```
   On Windows PowerShell:
   ```powershell
   Copy-Item .env.example .env
   ```
2. Edit `.env` for your environment (especially `SECRET_KEY`, DB settings, CORS).

## 3. Build and Start Stack

```bash
docker compose up -d --build
```

This starts:
- `frontend` (Nginx + Vite build) on `http://localhost:8080`
- `backend` (FastAPI) on `http://localhost:8000`
- `postgres`
- `redis`
- `celery-worker`
- `celery-beat`

Backend startup automatically runs:
1. `alembic upgrade head`
2. `python seed.py`
3. `uvicorn app.main:app ...`

## 4. Verify Deployment

Run:
```bash
docker compose ps
```

Check health:
- Frontend: `http://localhost:8080`
- Backend health: `http://localhost:8000/api/health`
- Backend docs: `http://localhost:8000/docs`
- Frontend API proxy health: `http://localhost:8080/api/health`

Tail logs:
```bash
docker compose logs -f backend
docker compose logs -f frontend
docker compose logs -f celery-worker
```

## 5. Common Operations

Restart services:
```bash
docker compose restart backend frontend
```

Rebuild a single service:
```bash
docker compose up -d --build frontend
docker compose up -d --build backend
```

Run migrations manually:
```bash
docker compose exec backend alembic upgrade head
```

Reseed data:
```bash
docker compose exec backend python seed.py
```

Stop stack:
```bash
docker compose down
```

Stop and remove volumes (deletes DB data):
```bash
docker compose down -v
```

## 6. Production Notes

- Replace default credentials and `SECRET_KEY`.
- Restrict `CORS_ORIGINS` to real domains.
- Do not expose PostgreSQL/Redis publicly unless required.
- Use HTTPS and reverse proxy (Traefik/Nginx/Caddy) in production.
- Use persistent volume backups for `postgres_data`.

## 7. Troubleshooting

- Frontend not reflecting changes:
  - Rebuild frontend image and hard refresh browser (`Ctrl+F5`).
- `500` from `/api/auth/me`:
  - Check backend logs and DB migrations (`docker compose logs backend`).
- Missing tables/columns:
  - Ensure Alembic ran successfully (`docker compose exec backend alembic upgrade head`).
- Port conflict:
  - Change host ports in `docker-compose.yml` and restart.
