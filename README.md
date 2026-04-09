# Cacao Backend

A full-stack cacao monitoring project with a Vue 3 frontend and a FastAPI backend.

## Stack

- Vue 3 + Vite frontend
- FastAPI backend
- PostgreSQL database
- Alembic migrations
- Redis
- Celery worker and beat
- Docker Compose deployment

## Features

- User and admin login flows
- Device management
- Sensor readings and history
- Alert tracking
- Analytics and dashboard views
- Background sensor-data generation and alert checks
- Seeded development data

## Local Setup

### Frontend

```bash
npm install
npm run dev
```

Frontend URL:
- `http://127.0.0.1:5173`

### Backend

Create and activate a virtual environment, then install dependencies:

```bash
py -3 -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Run migrations:

```bash
alembic upgrade head
```

Seed sample data:

```bash
python seed.py
```

Start the API:

```bash
uvicorn app.main:app --reload
```

Backend URLs:
- API docs: `http://127.0.0.1:8000/docs`
- Health: `http://127.0.0.1:8000/api/health`

## Docker Usage

Build and start the full stack:

```bash
docker compose up --build
```

Services:
- Frontend: `http://localhost:8080`
- Backend docs: `http://localhost:8000/docs`
- Backend health: `http://localhost:8000/api/health`

What happens on backend container startup:
1. Alembic migrations are applied
2. `seed.py` runs
3. FastAPI starts

Celery beat is configured to:
- generate demo sensor readings every 2 minutes
- check alerts every minute

Stop the stack:

```bash
docker compose down
```

Remove containers and volumes:

```bash
docker compose down -v
```

## Environment Variables

Copy `.env.example` to `.env` and adjust values as needed.

Important variables:
- `DATABASE_URL`
- `SYNC_DATABASE_URL`
- `REDIS_URL`
- `SECRET_KEY`
- `VITE_API_BASE_URL`
- `VITE_THINGSPEAK_READ_API_KEY`
- `VITE_THINGSPEAK_CHANNEL_ID`

## Seeded Accounts

- Admin:
  - email: `admin@cacaomonitor.local`
  - password: `admin123`
- User:
  - email: `user@cacaomonitor.local`
  - password: `user123`

## Notes

- `.env` is intentionally excluded from Git
- generated files like `dist/` and local database artifacts are ignored
- this repo includes both the frontend and backend application code
