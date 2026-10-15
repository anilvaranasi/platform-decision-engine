from typing import Dict, List, Optional
from pydantic import BaseModel, Field

class JevNoulAnswer(BaseModel):
    probability: float = Field(ge=0.0, le=1.0)
    verdict: bool

class JevChoiceAnswer(BaseModel):
    chosen: str
    confidence: float = Field(ge=0.0, le=1.0)
    distribution: Dict[str, float] = Field(default_factory=dict)

from typing import Dict, List, Optional, Union

class JevScoreAnswer(BaseModel):
    score: float
    confidence: float = Field(ge=0.0, le=1.0)
    level_probabilities: Union[List[float], Dict[str, float]] = Field(default_factory=dict)

class JevValidationResult(BaseModel):
    success: bool
    is_valid_architecture: JevNoulAnswer
    is_governance_compliant: JevNoulAnswer
    primary_platform_fit: JevChoiceAnswer
    architecture_alignment_score: JevScoreAnswer
    verdict_summary: str
    model: str = "jev-latest"
    mode: str = Field(description="live_api | calibrated_engine")
    error: Optional[str] = None
