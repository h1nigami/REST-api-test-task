from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.services import ActivityService
from app.schemas.activities import (
    ActivityCreate, ActivityUpdate, ActivityResponse, ActivityTreeResponse
)

router = APIRouter(prefix="/activities", tags=["activities"])

def get_activity_service(db: AsyncSession = Depends(get_db)) -> ActivityService:
    return ActivityService(db)

@router.get("/", response_model=List[ActivityResponse])
async def get_activities(
    skip: int = 0,
    limit: int = 100,
    service: ActivityService = Depends(get_activity_service)
):
    """Получить список видов деятельности"""
    activities = await service.get_activities(skip, limit)
    return [ActivityResponse(**act) for act in activities]

@router.get("/{activity_id}", response_model=ActivityResponse)
async def get_activity(
    activity_id: int,
    service: ActivityService = Depends(get_activity_service)
):
    """Получить вид деятельности по ID"""
    activity = await service.get_activity(activity_id)
    if not activity:
        raise HTTPException(status_code=404, detail="Вид деятельности не найден")
    return ActivityResponse(**activity)

@router.get("/{activity_id}/tree", response_model=ActivityTreeResponse)
async def get_activity_with_children(
    activity_id: int,
    service: ActivityService = Depends(get_activity_service)
):
    """Получить вид деятельности с дочерними элементами"""
    activity = await service.get_activity_with_children(activity_id)
    if not activity:
        raise HTTPException(status_code=404, detail="Вид деятельности не найден")
    return ActivityTreeResponse(**activity)

@router.post("/", response_model=ActivityResponse, status_code=201)
async def create_activity(
    activity: ActivityCreate,
    service: ActivityService = Depends(get_activity_service)
):
    """Создать новый вид деятельности"""
    try:
        created = await service.create_activity(activity)
        return ActivityResponse(**created)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{activity_id}", response_model=ActivityResponse)
async def update_activity(
    activity_id: int,
    activity: ActivityUpdate,
    service: ActivityService = Depends(get_activity_service)
):
    """Обновить вид деятельности"""
    updated = await service.update_activity(activity_id, activity)
    if not updated:
        raise HTTPException(status_code=404, detail="Вид деятельности не найден")
    return ActivityResponse(**updated)

@router.delete("/{activity_id}", status_code=204)
async def delete_activity(
    activity_id: int,
    service: ActivityService = Depends(get_activity_service)
):
    """Удалить вид деятельности"""
    try:
        success = await service.delete_activity(activity_id)
        if not success:
            raise HTTPException(status_code=404, detail="Вид деятельности не найден")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/tree/all", response_model=List[ActivityTreeResponse])
async def get_activity_tree(
    service: ActivityService = Depends(get_activity_service)
):
    """Получить полное дерево видов деятельности"""
    tree = await service.get_activity_tree()
    return [ActivityTreeResponse(**item) for item in tree]