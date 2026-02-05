from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class ActivityBase(BaseModel):
    name: str
    description: Optional[str] = None
    parent_id: Optional[int] = None

class ActivityCreate(ActivityBase):
    pass

class ActivityUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    parent_id: Optional[int] = None

class ActivityResponse(ActivityBase):
    id: int
    
    class Config:
        from_attributes = True

class ActivityTreeResponse(ActivityResponse):
    children: List[ActivityTreeResponse] = []
    
    class Config:
        from_attributes = True