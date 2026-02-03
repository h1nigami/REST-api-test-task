from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List

class OrganizationSimple(BaseModel):
    id: int
    name: str
    
    model_config = ConfigDict(from_attributes=True)

class OrganizationDetail(OrganizationSimple):
    description: Optional[str] = None
    building: Optional['BuildingSimple'] = None
    activities: List['ActivitySimple'] = []
    
    model_config = ConfigDict(from_attributes=True)

class OrganizationWithDistance(OrganizationDetail):
    distance_km: float
    
    model_config = ConfigDict(from_attributes=True)