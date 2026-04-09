# Validation Report

Date: 2026-04-09
Environment: `127.0.0.1` / local development

## Overall Status

The backend stack is working end to end with:

- FastAPI
- PostgreSQL
- Alembic migrations
- Redis
- Celery worker
- Celery beat
- Seeded sample data

## Database Status

Database:
- `cacao`

Extension enabled:
- `pgcrypto`

Tables verified:
- `alembic_version`
- `users`
- `devices`
- `refresh_tokens`
- `sensor_readings`
- `device_alerts`

## Row Counts

Current verified row counts:

- `users`: `2`
- `devices`: `1`
- `sensor_readings`: `25`
- `device_alerts`: `4`

Seeded users:
- `System Administrator` / `admin@cacaomonitor.local` / role `admin`
- `Normal User` / `user@cacaomonitor.local` / role `user`

## API Status

FastAPI health check:
- `GET http://127.0.0.1:8000/api/health`
- Response: `{"status":"ok"}`

Swagger docs:
- `http://127.0.0.1:8000/docs`

## Redis Status

Redis is installed and running locally.

Validation:
- `redis-cli ping`
- Response: `PONG`

Redis URL:
- `redis://localhost:6379/0`

## Celery Status

Celery services are running:

- worker
- beat

Verified tasks:
- `app.celery_app.generate_fake_sensor_data`
- `app.celery_app.check_alerts`
- `app.celery_app.ping`

Execution checks completed successfully:

- `generate_fake_sensor_data.delay(1)` created a new sensor reading
- `check_alerts.delay()` created a new alert

## Background Job Verification

After triggering Celery tasks:

- sensor readings increased from `24` to `25`
- alerts increased from `3` to `4`

Latest reading observed:
- device id: `1`
- timestamp: `2026-04-09T19:37:28.451171+08:00`
- temperature: `47.75`
- moisture: `8.22`
- ambient temp: `34.31`

Latest generated alert:
- type: `Ambient Temperature`
- severity: `warning`
- message: `Ambient temperature warning at 34.31 C.`

Device status after task execution:
- device id: `1`
- online: `true`
- `last_seen` updated successfully

## Conclusion

The system is validated and operational in local development.

Working components:
- PostgreSQL connection and schema
- Alembic-applied tables
- Seeded users, device, readings, and alerts
- FastAPI API server
- Redis broker/backend
- Celery task execution

Primary local endpoint:
- `http://127.0.0.1:8000/docs`
