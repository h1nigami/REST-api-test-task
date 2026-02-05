from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.organizations_repository import OrganizationRepository
from app.repositories.buildings_repository import BuildingRepository
from app.repositories.activities_repositoriy import ActivityRepository
from app.schemas.organization import OrganizationCreate, OrganizationUpdate

class OrganizationService:
    def __init__(self, session: AsyncSession):
        self.organization_repo = OrganizationRepository(session)
        self.building_repo = BuildingRepository(session)
        self.activity_repo = ActivityRepository(session)
    
    async def get_organizations(self, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        return await self.organization_repo.get_all(skip, limit)
    
    async def get_organization(self, organization_id: int) -> Optional[Dict[str, Any]]:
        return await self.organization_repo.get(organization_id)
    
    async def get_organization_with_details(self, organization_id: int) -> Optional[Dict[str, Any]]:
        return await self.organization_repo.get_with_details(organization_id)
    
    async def create_organization(self, organization: OrganizationCreate) -> Dict[str, Any]:
        # Проверяем уникальность названия
        existing_name = await self.organization_repo.get_by_name(organization.name)
        if existing_name:
            raise ValueError(f"Организация с названием '{organization.name}' уже существует")
        
        # Проверяем уникальность телефона
        existing_phone = await self.organization_repo.get_by_phone(organization.phone_number)
        if existing_phone:
            raise ValueError(f"Организация с телефоном '{organization.phone_number}' уже существует")
        
        return await self.organization_repo.create(organization)
    
    async def update_organization(self, organization_id: int, organization: OrganizationUpdate) -> Optional[Dict[str, Any]]:
        return await self.organization_repo.update(organization_id, organization)
    
    async def delete_organization(self, organization_id: int) -> bool:
        return await self.organization_repo.delete(organization_id)
    
    async def get_organizations_by_building(self, building_id: int) -> List[Dict[str, Any]]:
        return await self.organization_repo.get_by_building(building_id)
    
    async def add_activity_to_organization(
        self, 
        organization_id: int, 
        activity_id: int, 
        is_primary: bool = False
    ) -> bool:
        # Проверяем существование организации
        org = await self.organization_repo.get(organization_id)
        if not org:
            raise ValueError(f"Организация с ID {organization_id} не найдена")
        
        # Проверяем существование вида деятельности
        activity = await self.activity_repo.get(activity_id)
        if not activity:
            raise ValueError(f"Вид деятельности с ID {activity_id} не найден")
        
        return await self.organization_repo.add_activity(organization_id, activity_id, is_primary)
    
    async def remove_activity_from_organization(self, organization_id: int, activity_id: int) -> bool:
        return await self.organization_repo.remove_activity(organization_id, activity_id)