from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.database import AsyncSessionLocal, engine
from app.models import Base
from app.routers import alerts, auth, devices, health, iot, sensor_readings, user, user_settings
from app.services.auth import ensure_default_admin_user


settings = get_settings()
uploads_dir = Path("uploads")
uploads_dir.mkdir(parents=True, exist_ok=True)


@asynccontextmanager
async def lifespan(_: FastAPI):
    async with engine.begin() as connection:
        await connection.execute(text("SELECT 1"))
        await connection.run_sync(Base.metadata.create_all)

    db: AsyncSession = AsyncSessionLocal()
    try:
        await ensure_default_admin_user(db)
    finally:
        await db.close()
    yield


app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    lifespan=lifespan,
)
app.mount("/uploads", StaticFiles(directory=uploads_dir), name="uploads")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in settings.cors_origins.split(",") if origin.strip()],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix=settings.api_prefix, tags=["Health"])
app.include_router(auth.router, prefix=settings.api_prefix, tags=["Auth"])
app.include_router(user.router, prefix=settings.api_prefix, tags=["User"])
app.include_router(devices.router, prefix=settings.api_prefix, tags=["Devices"])
app.include_router(sensor_readings.router, prefix=settings.api_prefix, tags=["Sensor Readings"])
app.include_router(alerts.router, prefix=settings.api_prefix, tags=["Alerts"])
app.include_router(iot.router, prefix=settings.api_prefix, tags=["IoT Ingest"])
app.include_router(user_settings.router, prefix=settings.api_prefix, tags=["User Settings"])
