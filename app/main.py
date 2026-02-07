from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core.database import engine, Base
from app.api.v1 import activities, buildings, organization

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Создание таблиц при запуске
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("База данных инициализирована")
    yield
    # Очистка при завершении
    await engine.dispose()

app = FastAPI(
    title="Building Management API",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(buildings.router, prefix="/api/v1", tags=["buildings"])
app.include_router(organization.router, prefix="/api/v1", tags=["organizations"])
app.include_router(activities.router, prefix="/api/v1", tags=["activities"])

@app.get("/")
async def root():
    return {
        "message": "Building Management API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/seed")
async def seed():
    """Заполнение бд тестовыми данными"""
    from .scripts import seed_database as seed
    await seed.seed_database()
    return {"message": "База данных заполнена"}