from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from src.models.request import RequestContext
from src.models.jev import JevValidationResult

class StageRecommendation(BaseModel):
    stage_number: int
    stage_name: str
    phase: str
    platform_id: str
    platform_name: str
    platform_tier: str
    capability_id: str
    action: str
    rationale: str
    features_utilized: List[str] = Field(default_factory=list)

class AlternativePlatform(BaseModel):
    platform_id: str
    platform_name: str
    score: float
    reason: str

class DecisionBlueprint(BaseModel):
    initiative_name: Optional[str] = None
    request: RequestContext
    decision_type: str = Field(description="rule_matched | capability_scored | fallback")
    matched_rule_id: Optional[str] = None
    matched_rule_name: Optional[str] = None
    stages: List[StageRecommendation] = Field(default_factory=list)
    architecture_summary: str
    recommended_integrations: List[str] = Field(default_factory=list)
    alternatives_considered: List[AlternativePlatform] = Field(default_factory=list)
    jev_validation: Optional[JevValidationResult] = Field(default=None, description="TypeSafe Jev System One verification verdict")
    metadata: Dict[str, Any] = Field(default_factory=dict)
