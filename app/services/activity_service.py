from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.activities_repositoriy import ActivityRepository
from app.schemas.activities import ActivityCreate, ActivityUpdate

class ActivityService:
    def __init__(self, session: AsyncSession):
        self.repository = ActivityRepository(session)
    
    async def get_activities(self, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        return await self.repository.get_all(skip, limit)
    
    async def get_activity(self, activity_id: int) -> Optional[Dict[str, Any]]:
        return await self.repository.get(activity_id)
    
    async def get_activity_with_children(self, activity_id: int) -> Optional[Dict[str, Any]]:
        return await self.repository.get_with_children(activity_id)
    
    async def create_activity(self, activity: ActivityCreate) -> Dict[str, Any]:
        # Проверяем уникальность названия
        existing = await self.repository.get_by_name(activity.name)
        if existing:
            raise ValueError(f"Вид деятельности с названием '{activity.name}' уже существует")
        
        return await self.repository.create(activity)
    
    async def update_activity(self, activity_id: int, activity: ActivityUpdate) -> Optional[Dict[str, Any]]:
        return await self.repository.update(activity_id, activity)
    
    async def delete_activity(self, activity_id: int) -> bool:
        activity = await self.repository.get_with_children(activity_id)
        if activity and activity.get('children'):
            raise ValueError("Нельзя удалить вид деятельности с дочерними элементами")
        
        return await self.repository.delete(activity_id)
    
    async def get_activity_tree(self) -> List[Dict[str, Any]]:
        return await self.repository.get_tree()