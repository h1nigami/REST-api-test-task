from fastapi import FastAPI
import asyncio
from .core.database import engine, Base
from .models import *

app = FastAPI()


@app.on_event("startup")
async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

