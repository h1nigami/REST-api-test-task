from typing import TypeVar, Type, Optional, List, Dict, Any, Generic
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update as sql_update, delete as sql_delete
from sqlalchemy.orm import class_mapper
from pydantic import BaseModel

ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class BaseRepository(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType], session: AsyncSession):
        self.model = model
        self.session = session
    
    def _to_dict(self, obj: ModelType) -> Dict[str, Any]:
        """Convert SQLAlchemy model to dict"""
        if not obj:
            return {}
        return {c.key: getattr(obj, c.key) for c in class_mapper(obj.__class__).columns}
    
    async def get(self, id: int) -> Optional[Dict[str, Any]]:
        result = await self.session.execute(
            select(self.model).where(self.model.id == id)
        )
        obj = result.scalar_one_or_none()
        return self._to_dict(obj) if obj else None
    
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        result = await self.session.execute(
            select(self.model).offset(skip).limit(limit)
        )
        return [self._to_dict(obj) for obj in result.scalars().all()]
    
    async def create(self, obj_in: CreateSchemaType) -> Dict[str, Any]:
        db_obj = self.model(**obj_in.model_dump(exclude_unset=True))
        self.session.add(db_obj)
        await self.session.flush()
        await self.session.refresh(db_obj)
        return self._to_dict(db_obj)
    
    async def update(self, id: int, obj_in: UpdateSchemaType) -> Optional[Dict[str, Any]]:
        # Получаем объект
        result = await self.session.execute(
            select(self.model).where(self.model.id == id)
        )
        db_obj = result.scalar_one_or_none()
        if not db_obj:
            return None
        
        # Обновляем поля
        update_data = obj_in.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        
        self.session.add(db_obj)
        await self.session.flush()
        await self.session.refresh(db_obj)
        return self._to_dict(db_obj)
    
    async def delete(self, id: int) -> bool:
        result = await self.session.execute(
            select(self.model).where(self.model.id == id)
        )
        db_obj = result.scalar_one_or_none()
        if not db_obj:
            return False
        
        await self.session.delete(db_obj)
        await self.session.flush()
        return True
    
    async def count(self) -> int:
        from sqlalchemy import func
        result = await self.session.execute(
            select(func.count(self.model.id))
        )
        return result.scalar() or 0