from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.database import AsyncSessionLocal, engine
from app.models import Base
from app.routers import alerts, auth, devices, health, sensor_readings
from app.services.auth import ensure_default_admin_user


settings = get_settings()


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

app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in settings.cors_origins.split(",") if origin.strip()],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix=settings.api_prefix, tags=["Health"])
app.include_router(auth.router, prefix=settings.api_prefix, tags=["Auth"])
app.include_router(devices.router, prefix=settings.api_prefix, tags=["Devices"])
app.include_router(sensor_readings.router, prefix=settings.api_prefix, tags=["Sensor Readings"])
app.include_router(alerts.router, prefix=settings.api_prefix, tags=["Alerts"])
