from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.health_router import router as health_router
from app.api.dataset_router import router as dataset_router
from app.config.database import create_db_and_tables
from app.config.settings import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    print('Database Created ...')
    yield


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    lifespan=lifespan,
)

app.include_router(health_router)
app.include_router(dataset_router)

@app.get("/")
def root():
    return {
        "project": settings.app_name,
        "version": settings.app_version,
        "status": "running",
    }