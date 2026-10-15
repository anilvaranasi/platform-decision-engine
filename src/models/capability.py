from typing import List, Optional
from pydantic import BaseModel, Field

class SubCapability(BaseModel):
    id: str
    name: str
    category: str = Field(description="engagement | record | intelligence | orchestration")

class Capability(BaseModel):
    id: str
    name: str
    description: str
    category: Optional[str] = None
    sub_capabilities: List[SubCapability] = Field(default_factory=list)

class Domain(BaseModel):
    id: str
    name: str
    capabilities: List[Capability] = Field(default_factory=list)
