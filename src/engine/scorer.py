import re
from typing import List, Dict, Optional, Tuple
from src.models.platform import Platform, PlatformCapability
from src.models.request import RequestContext, IntentType
from src.models.decision import AlternativePlatform

class ScoringEngine:
    """Multi-Criteria Decision Analysis (MCDA) Scoring Engine for Platforms."""

    def __init__(self, platforms: Dict[str, Platform]):
        self.platforms = platforms

    def score_platform_for_capability(
        self,
        platform: Platform,
        capability_id: str,
        required_features: List[str] = None,
        intent: Optional[IntentType] = None,
    ) -> Tuple[float, List[str]]:
        """
        Calculates a score between 0.0 and 1.0 for a platform against a capability.
        Returns (score, list of matched features).
        """
        required_features = required_features or []
        target_cap = capability_id.lower().strip()
        matched_cap: Optional[PlatformCapability] = None

        # 1. Exact match
        for cap in platform.capabilities:
            if cap.capability_id.lower() == target_cap:
                matched_cap = cap
                break

        # 2. Prefix or substring match if no exact match (e.g. "hr.onboarding" matches "hr.onboarding.workflow")
        if not matched_cap:
            for cap in platform.capabilities:
                if cap.capability_id.lower().startswith(target_cap) or target_cap.startswith(cap.capability_id.lower()):
                    matched_cap = cap
                    break

        if not matched_cap:
            return 0.0, []

        base_strength = matched_cap.strength
        score = base_strength

        # Feature matching bonus / weight
        matched_features = []
        if required_features:
            req_set = {f.lower() for f in required_features}
            avail_set = {f.lower() for f in matched_cap.features}
            common = req_set.intersection(avail_set)
            matched_features = list(common)
            feature_ratio = len(common) / len(req_set) if req_set else 1.0
            score = (base_strength * 0.7) + (feature_ratio * 0.3)
        else:
            matched_features = matched_cap.features

        # Architecture Tier Alignment Adjustments
        if intent == IntentType.BUILD_NEW and "System of Engagement" in platform.tier:
            score = min(1.0, score + 0.05)
        elif intent == IntentType.UPDATE_CORE_PROCESS and "System of Record" in platform.tier:
            score = min(1.0, score + 0.05)

        return round(score, 3), matched_features

    def rank_platforms(
        self,
        request: RequestContext,
    ) -> List[AlternativePlatform]:
        """Ranks all platforms for a given request context."""
        ranked: List[AlternativePlatform] = []

        for p in self.platforms.values():
            score, features = self.score_platform_for_capability(
                platform=p,
                capability_id=request.capability,
                required_features=request.required_features,
                intent=request.intent,
            )

            if score > 0.0:
                reason = f"Tier: {p.tier} | Base Strength: {p.capability_strength(request.capability)} | Matched Features: {', '.join(features[:3]) if features else 'Standard'}"
                ranked.append(
                    AlternativePlatform(
                        platform_id=p.id,
                        platform_name=p.name,
                        score=score,
                        reason=reason,
                    )
                )

        ranked.sort(key=lambda x: x.score, reverse=True)
        return ranked
