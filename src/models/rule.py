from typing import List, Optional
from pydantic import BaseModel, Field

class RuleCondition(BaseModel):
    domain: Optional[str] = None
    capability: Optional[str] = None
    capability_pattern: Optional[str] = None
    intent: Optional[str] = None

class RuleStage(BaseModel):
    phase: str
    stage_name: str
    platform_id: str
    capability_id: str
    action: str
    rationale: str

class DecisionRule(BaseModel):
    id: str
    name: str
    description: str
    priority: int = Field(default=0, description="Higher number takes precedence")
    conditions: RuleCondition
    stages: List[RuleStage] = Field(default_factory=list)
