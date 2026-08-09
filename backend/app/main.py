from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.health_router import router as health_router
from app.api.dataset_router import router as dataset_router
from app.api.monitoring_router import router as monitoring_router
from app.api.threshold_router import router as threshold_router
from app.api.alert_router import router as alert_router
from app.config.database import create_db_and_tables
from app.config.settings import settings
from app.api.alert_router import (
    router as alert_router,
)
from app.scheduler.scheduler import (
    start_scheduler,
    stop_scheduler,
)
from app.api.data_source_router import router as data_source_router
@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    start_scheduler()
    print('Database Created ...')
    yield
    stop_scheduler()


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    lifespan=lifespan,
)

app.include_router(health_router)
app.include_router(dataset_router)
app.include_router(monitoring_router)
app.include_router(threshold_router)
app.include_router(alert_router)
app.include_router(alert_router)
app.include_router(data_source_router)

@app.get("/")
def root():
    return {
        "project": settings.app_name,
        "version": settings.app_version,
        "status": "running",
    }