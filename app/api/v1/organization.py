from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.services import OrganizationService
from app.schemas.organization import (
    OrganizationCreate, OrganizationUpdate, OrganizationResponse, OrganizationWithDetails
)

router = APIRouter(prefix="/organizations", tags=["organizations"])

def get_organization_service(db: AsyncSession = Depends(get_db)) -> OrganizationService:
    return OrganizationService(db)

@router.get("/", response_model=List[OrganizationResponse])
async def get_organizations(
    skip: int = 0,
    limit: int = 100,
    service: OrganizationService = Depends(get_organization_service)
):
    """Получить список организаций"""
    organizations = await service.get_organizations(skip, limit)
    return [OrganizationResponse(**org) for org in organizations]

@router.get("/{organization_id}", response_model=OrganizationResponse)
async def get_organization(
    organization_id: int,
    service: OrganizationService = Depends(get_organization_service)
):
    """Получить организацию по ID"""
    organization = await service.get_organization(organization_id)
    if not organization:
        raise HTTPException(status_code=404, detail="Организация не найдена")
    return OrganizationResponse(**organization)

@router.get("/{organization_id}/with-details", response_model=OrganizationWithDetails)
async def get_organization_with_details(
    organization_id: int,
    service: OrganizationService = Depends(get_organization_service)
):
    """Получить организацию с деталями (здание и виды деятельности)"""
    organization = await service.get_organization_with_details(organization_id)
    if not organization:
        raise HTTPException(status_code=404, detail="Организация не найдена")
    return OrganizationWithDetails(**organization)

@router.post("/", response_model=OrganizationResponse, status_code=201)
async def create_organization(
    organization: OrganizationCreate,
    service: OrganizationService = Depends(get_organization_service)
):
    """Создать новую организацию"""
    try:
        created = await service.create_organization(organization)
        return OrganizationResponse(**created)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{organization_id}", response_model=OrganizationResponse)
async def update_organization(
    organization_id: int,
    organization: OrganizationUpdate,
    service: OrganizationService = Depends(get_organization_service)
):
    """Обновить организацию"""
    updated = await service.update_organization(organization_id, organization)
    if not updated:
        raise HTTPException(status_code=404, detail="Организация не найдена")
    return OrganizationResponse(**updated)

@router.delete("/{organization_id}", status_code=204)
async def delete_organization(
    organization_id: int,
    service: OrganizationService = Depends(get_organization_service)
):
    """Удалить организацию"""
    success = await service.delete_organization(organization_id)
    if not success:
        raise HTTPException(status_code=404, detail="Организация не найдена")

@router.get("/building/{building_id}", response_model=List[OrganizationResponse])
async def get_organizations_by_building(
    building_id: int,
    service: OrganizationService = Depends(get_organization_service)
):
    """Получить организации по зданию"""
    organizations = await service.get_organizations_by_building(building_id)
    return [OrganizationResponse(**org) for org in organizations]

@router.post("/{organization_id}/activities/{activity_id}")
async def add_activity_to_organization(
    organization_id: int,
    activity_id: int,
    is_primary: bool = False,
    service: OrganizationService = Depends(get_organization_service)
):
    """Добавить вид деятельности к организации"""
    try:
        success = await service.add_activity_to_organization(organization_id, activity_id, is_primary)
        if not success:
            raise HTTPException(status_code=400, detail="Не удалось добавить вид деятельности")
        return {"message": "Вид деятельности успешно добавлен"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{organization_id}/activities/{activity_id}")
async def remove_activity_from_organization(
    organization_id: int,
    activity_id: int,
    service: OrganizationService = Depends(get_organization_service)
):
    """Удалить вид деятельности у организации"""
    success = await service.remove_activity_from_organization(organization_id, activity_id)
    if not success:
        raise HTTPException(status_code=404, detail="Связь не найдена")
    return {"message": "Вид деятельности успешно удален"}