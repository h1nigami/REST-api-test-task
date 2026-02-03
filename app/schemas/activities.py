from pydantic import BaseModel, Field, ConfigDict
from typing import List

class ActivitySimple(BaseModel):
    id: int
    name: str
    level: int
    
    model_config = ConfigDict(from_attributes=True)

class ActivityTree(ActivitySimple):
    children: List['ActivityTree'] = []
    
    model_config = ConfigDict(from_attributes=True)

ActivityTree.model_rebuild()