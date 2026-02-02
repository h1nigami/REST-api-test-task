from models.building import Building
from sqlalchemy.ext.asyncio import AsyncSession


class BuildingsRepository:

    def create(self, db:AsyncSession, building:Building):
        db.add(building)
        return building