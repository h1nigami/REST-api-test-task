from typing import Optional, List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from sqlalchemy.orm import selectinload

from app.models.building import Building
from app.schemas.building import BuildingCreate, BuildingUpdate
from .base import BaseRepository

class BuildingRepository(BaseRepository[Building, BuildingCreate, BuildingUpdate]):
    def __init__(self, session: AsyncSession):
        super().__init__(Building, session)
    
    async def get_with_organizations(self, building_id: int) -> Optional[Dict[str, Any]]:
        result = await self.session.execute(
            select(Building)
            .where(Building.id == building_id)
            .options(selectinload(Building.organizations))
        )
        building = result.scalar_one_or_none()
        if not building:
            return None
        
        data = self._to_dict(building)
        data['organizations'] = [
            {"id": org.id, "name": org.name, "phone_number": org.phone_number}
            for org in building.organizations
        ]
        return data
    
    async def get_by_address(self, address: str) -> Optional[Dict[str, Any]]:
        result = await self.session.execute(
            select(Building).where(Building.address == address)
        )
        building = result.scalar_one_or_none()
        return self._to_dict(building) if building else None
    
    async def search_by_location(
        self, 
        min_lat: float, 
        max_lat: float, 
        min_lon: float, 
        max_lon: float
    ) -> List[Dict[str, Any]]:
        result = await self.session.execute(
            select(Building).where(
                and_(
                    Building.latitude.between(min_lat, max_lat),
                    Building.longitude.between(min_lon, max_lon)
                )
            )
        )
        return [self._to_dict(building) for building in result.scalars().all()]