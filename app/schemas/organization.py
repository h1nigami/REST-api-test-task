from __future__ import annotations
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime

class OrganizationBase(BaseModel):
    name: str
    phone_number: str
    description: Optional[str] = None
    building_id: Optional[int] = None

class OrganizationCreate(OrganizationBase):
    @field_validator('phone_number')
    def validate_phone(cls, v):
        digits = ''.join(filter(str.isdigit, v))
        if len(digits) < 10:
            raise ValueError('Номер телефона должен содержать минимум 10 цифр')
        return v

class OrganizationUpdate(BaseModel):
    name: Optional[str] = None
    phone_number: Optional[str] = None
    description: Optional[str] = None
    building_id: Optional[int] = None

class OrganizationResponse(OrganizationBase):
    id: int
    
    class Config:
        from_attributes = True

class OrganizationWithDetails(OrganizationResponse):
    building: Optional[dict] = None
    activities: List[dict] = []
    
    class Config:
        from_attributes = True