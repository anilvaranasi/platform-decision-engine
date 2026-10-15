from typing import List, Dict, Optional
from pydantic import BaseModel, Field

class PlatformCapability(BaseModel):
    capability_id: str
    strength: float = Field(ge=0.0, le=1.0, description="Strength score between 0.0 and 1.0")
    features: List[str] = Field(default_factory=list, description="Specific features offered by this platform")

class Platform(BaseModel):
    id: str
    name: str
    description: str
    tier: str = Field(description="Architecture tier e.g. System of Record, System of Engagement, Intelligence")
    vendor_type: Optional[str] = None
    capabilities: List[PlatformCapability] = Field(default_factory=list)
    constraints: List[str] = Field(default_factory=list)

    def get_capability(self, capability_id: str) -> Optional[PlatformCapability]:
        for cap in self.capabilities:
            if cap.capability_id == capability_id:
                return cap
        return None

    def has_capability(self, capability_id: str) -> bool:
        return self.get_capability(capability_id) is not None

    def capability_strength(self, capability_id: str) -> float:
        cap = self.get_capability(capability_id)
        return cap.strength if cap else 0.0
