from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class BuildingBase(BaseModel):
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    address: str

class BuildingCreate(BuildingBase):
    pass

class BuildingUpdate(BaseModel):
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    address: Optional[str] = None

class BuildingResponse(BuildingBase):
    id: int
    
    class Config:
        from_attributes = True

class BuildingWithOrganizations(BuildingResponse):
    organizations: List[dict] = []
    
    class Config:
        from_attributes = True