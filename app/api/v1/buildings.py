from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.services import BuildingService
from app.schemas.building import (
    BuildingCreate, BuildingUpdate, BuildingResponse, BuildingWithOrganizations
)

router = APIRouter(prefix="/buildings", tags=["buildings"])

def get_building_service(db: AsyncSession = Depends(get_db)) -> BuildingService:
    return BuildingService(db)

@router.get("/", response_model=List[BuildingResponse])
async def get_buildings(
    skip: int = 0,
    limit: int = 100,
    service: BuildingService = Depends(get_building_service)
):
    """Получить список зданий"""
    buildings = await service.get_buildings(skip, limit)
    return [BuildingResponse(**b) for b in buildings]

@router.get("/{building_id}", response_model=BuildingResponse)
async def get_building(
    building_id: int,
    service: BuildingService = Depends(get_building_service)
):
    """Получить здание по ID"""
    building = await service.get_building(building_id)
    if not building:
        raise HTTPException(status_code=404, detail="Здание не найден")
    return BuildingResponse(**building)

@router.get("/{building_id}/with-organizations", response_model=BuildingWithOrganizations)
async def get_building_with_organizations(
    building_id: int,
    service: BuildingService = Depends(get_building_service)
):
    """Получить здание с организациями"""
    building = await service.get_building_with_organizations(building_id)
    if not building:
        raise HTTPException(status_code=404, detail="Здание не найден")
    return BuildingWithOrganizations(**building)

@router.post("/", response_model=BuildingResponse, status_code=201)
async def create_building(
    building: BuildingCreate,
    service: BuildingService = Depends(get_building_service)
):
    """Создать новое здание"""
    try:
        created = await service.create_building(building)
        return BuildingResponse(**created)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{building_id}", response_model=BuildingResponse)
async def update_building(
    building_id: int,
    building: BuildingUpdate,
    service: BuildingService = Depends(get_building_service)
):
    """Обновить здание"""
    updated = await service.update_building(building_id, building)
    if not updated:
        raise HTTPException(status_code=404, detail="Здание не найден")
    return BuildingResponse(**updated)

@router.delete("/{building_id}", status_code=204)
async def delete_building(
    building_id: int,
    service: BuildingService = Depends(get_building_service)
):
    """Удалить здание"""
    try:
        success = await service.delete_building(building_id)
        if not success:
            raise HTTPException(status_code=404, detail="Здание не найден")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/search/location", response_model=List[BuildingResponse])
async def search_buildings_by_location(
    min_lat: float = Query(...),
    max_lat: float = Query(...),
    min_lon: float = Query(...),
    max_lon: float = Query(...),
    service: BuildingService = Depends(get_building_service)
):
    """Поиск зданий по координатам"""
    buildings = await service.search_by_location(min_lat, max_lat, min_lon, max_lon)
    return [BuildingResponse(**b) for b in buildings]