from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field

class IntentType(str, Enum):
    BUILD_NEW = "build_new"
    OPTIMIZE_EXISTING = "optimize_existing"
    UPDATE_CORE_PROCESS = "update_core_process"
    MIGRATE = "migrate"
    INTEGRATE = "integrate"

class RequestContext(BaseModel):
    initiative_name: Optional[str] = Field(default=None, description="Name or title of the initiative")
    domain: str = Field(description="Target enterprise domain (e.g., HR, CRM, FINANCE, WORKFLOW)")
    capability: str = Field(description="Capability ID or keyword (e.g., hr.onboarding, crm.process, finance.payroll)")
    intent: IntentType = Field(default=IntentType.BUILD_NEW, description="Strategic intent")
    description: Optional[str] = Field(default=None, description="Free text description of the requirement")
    required_features: List[str] = Field(default_factory=list, description="Specific features required")
    constraints: List[str] = Field(default_factory=list, description="Any hard architectural or business constraints")
    requester: Optional[str] = Field(default=None, description="Team or architect requesting decision")
