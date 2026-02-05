from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.buildings_repository import BuildingRepository
from app.schemas.building import BuildingCreate, BuildingUpdate

class BuildingService:
    def __init__(self, session: AsyncSession):
        self.repository = BuildingRepository(session)
    
    async def get_buildings(self, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        return await self.repository.get_all(skip, limit)
    
    async def get_building(self, building_id: int) -> Optional[Dict[str, Any]]:
        return await self.repository.get(building_id)
    
    async def get_building_with_organizations(self, building_id: int) -> Optional[Dict[str, Any]]:
        return await self.repository.get_with_organizations(building_id)
    
    async def create_building(self, building: BuildingCreate) -> Dict[str, Any]:
        # Проверяем уникальность адреса
        existing = await self.repository.get_by_address(building.address)
        if existing:
            raise ValueError(f"Здание с адресом '{building.address}' уже существует")
        
        return await self.repository.create(building)
    
    async def update_building(self, building_id: int, building: BuildingUpdate) -> Optional[Dict[str, Any]]:
        return await self.repository.update(building_id, building)
    
    async def delete_building(self, building_id: int) -> bool:
        building = await self.repository.get_with_organizations(building_id)
        if building and building.get('organizations'):
            raise ValueError("Нельзя удалить здание, в котором есть организации")
        
        return await self.repository.delete(building_id)
    
    async def search_by_location(
        self, 
        min_lat: float, 
        max_lat: float, 
        min_lon: float, 
        max_lon: float
    ) -> List[Dict[str, Any]]:
        return await self.repository.search_by_location(min_lat, max_lat, min_lon, max_lon)