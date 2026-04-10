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

Detailed deployment walkthrough:
- See [DOCKER_DEPLOYMENT_GUIDE.md](./DOCKER_DEPLOYMENT_GUIDE.md)

## Environment Variables

Copy `.env.example` to `.env` and adjust values as needed.

Important variables:
- `DATABASE_URL`
- `SYNC_DATABASE_URL`
- `REDIS_URL`
- `SECRET_KEY`
- `VITE_API_BASE_URL`

## IoT Ingest Flow

1. Login as a user and create a device with `POST /api/devices`.
2. Save the returned `ingest_token` in the IoT firmware.
3. Upload readings to `POST /api/iot/readings` with header `X-Device-Token`.
4. Include `device_serial` in payload; backend verifies it matches the token-bound device.
5. Dashboard/history/analytics read from `/api/devices/{id}/readings...` endpoints.

## Seeded Accounts

- Admin:
  - email: `admin@cacaomonitor.local`
  - password: `admin123`
- User:
  - email: `user@cacaomonitor.local`
  - password: `user123`
- User:
  - email: `operator@cacaomonitor.local`
  - password: `operator123`
- User:
  - email: `qa@cacaomonitor.local`
  - password: `qauser123`

All seeded users receive default `user_settings` values:
- `theme_mode`: `system`
- `font_size`: `medium`
- `primary_color`: `#1f2937`
- `secondary_color`: `#526075`
- `accent_color`: `#f3a6ba`

## Notes

- `.env` is intentionally excluded from Git
- generated files like `dist/` and local database artifacts are ignored
- this repo includes both the frontend and backend application code
