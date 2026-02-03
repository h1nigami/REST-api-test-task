from pydantic import BaseModel, Field, ConfigDict
from typing import List

class BuildingSimple(BaseModel):
    id: int
    address: str
    latitude: float
    longitude: float
    
    model_config = ConfigDict(from_attributes=True)

class BuildingWithOrganizations(BuildingSimple):
    organizations: List['OrganizationSimple'] = []
    
    model_config = ConfigDict(from_attributes=True)