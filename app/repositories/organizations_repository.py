from typing import Optional, List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, delete
from sqlalchemy.orm import selectinload

from app.models.organization import Organization, organization_activities
from app.models.building import Building
from app.models.activities import Activity
from app.schemas.organization import OrganizationCreate, OrganizationUpdate
from .base import BaseRepository

class OrganizationRepository(BaseRepository[Organization, OrganizationCreate, OrganizationUpdate]):
    def __init__(self, session: AsyncSession):
        super().__init__(Organization, session)
    
    async def get_with_details(self, organization_id: int) -> Optional[Dict[str, Any]]:
        result = await self.session.execute(
            select(Organization)
            .where(Organization.id == organization_id)
            .options(
                selectinload(Organization.building),
                selectinload(Organization.activities)
            )
        )
        org = result.scalar_one_or_none()
        if not org:
            return None
        
        data = self._to_dict(org)
        data['building'] = self._to_dict(org.building) if org.building else None
        data['activities'] = [
            {"id": act.id, "name": act.name, "description": act.description}
            for act in org.activities
        ]
        return data
    
    async def get_by_phone(self, phone_number: str) -> Optional[Dict[str, Any]]:
        result = await self.session.execute(
            select(Organization).where(Organization.phone_number == phone_number)
        )
        org = result.scalar_one_or_none()
        return self._to_dict(org) if org else None
    
    async def get_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        result = await self.session.execute(
            select(Organization).where(Organization.name == name)
        )
        org = result.scalar_one_or_none()
        return self._to_dict(org) if org else None
    
    async def get_by_building(self, building_id: int) -> List[Dict[str, Any]]:
        result = await self.session.execute(
            select(Organization)
            .where(Organization.building_id == building_id)
            .options(selectinload(Organization.activities))
        )
        organizations = []
        for org in result.scalars().all():
            data = self._to_dict(org)
            data['activities'] = [
                {"id": act.id, "name": act.name}
                for act in org.activities
            ]
            organizations.append(data)
        return organizations
    
    async def add_activity(self, organization_id: int, activity_id: int, is_primary: bool = False) -> bool:
        stmt = insert(organization_activities).values(
            organization_id=organization_id,
            activity_id=activity_id,
            is_primary=is_primary
        ).on_conflict_do_nothing()
        
        await self.session.execute(stmt)
        await self.session.flush()
        return True
    
    async def remove_activity(self, organization_id: int, activity_id: int) -> bool:
        stmt = delete(organization_activities).where(
            (organization_activities.c.organization_id == organization_id) &
            (organization_activities.c.activity_id == activity_id)
        )
        
        result = await self.session.execute(stmt)
        await self.session.flush()
        return result.rowcount > 0