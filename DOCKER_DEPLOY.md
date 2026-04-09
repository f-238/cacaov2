# Docker Deployment

## Services

This project now includes a Docker Compose stack for:

- `frontend` via Nginx on port `8080`
- `backend` via FastAPI on port `8000`
- `postgres` on port `5432`
- `redis` on port `6379`
- `celery-worker`
- `celery-beat`

## Start

```bash
docker compose up --build
```

## URLs

- Frontend: `http://localhost:8080`
- Backend docs: `http://localhost:8000/docs`
- Backend health: `http://localhost:8000/api/health`

## What happens on startup

The backend container will:

1. apply Alembic migrations
2. run `seed.py`
3. start Uvicorn

Celery beat is configured to:

- generate demo sensor readings every 2 minutes
- run alert checks every minute

## Stop

```bash
docker compose down
```

To also remove volumes:

```bash
docker compose down -v
```
