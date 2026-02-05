from typing import Optional, List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.models.activities import Activity
from app.schemas.activities import ActivityCreate, ActivityUpdate
from .base import BaseRepository

class ActivityRepository(BaseRepository[Activity, ActivityCreate, ActivityUpdate]):
    def __init__(self, session: AsyncSession):
        super().__init__(Activity, session)
    
    async def get_with_children(self, activity_id: int) -> Optional[Dict[str, Any]]:
        result = await self.session.execute(
            select(Activity)
            .where(Activity.id == activity_id)
            .options(selectinload(Activity.children))
        )
        activity = result.scalar_one_or_none()
        if not activity:
            return None
        
        data = self._to_dict(activity)
        data['children'] = [self._to_dict(child) for child in activity.children]
        return data
    
    async def get_tree(self) -> List[Dict[str, Any]]:
        # Получаем корневые элементы
        result = await self.session.execute(
            select(Activity)
            .where(Activity.parent_id.is_(None))
            .options(selectinload(Activity.children))
        )
        
        def build_tree(activity: Activity) -> Dict[str, Any]:
            data = self._to_dict(activity)
            data['children'] = [build_tree(child) for child in activity.children]
            return data
        
        return [build_tree(activity) for activity in result.scalars().all()]
    
    async def get_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        result = await self.session.execute(
            select(Activity).where(Activity.name == name)
        )
        activity = result.scalar_one_or_none()
        return self._to_dict(activity) if activity else None