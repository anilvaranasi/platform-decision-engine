from typing import List, Optional
from src.engine.catalog import Catalog, CatalogLoader
from src.engine.rule_evaluator import RuleEvaluator
from src.engine.scorer import ScoringEngine
from src.engine.jev_validator import JevValidator
from src.models.request import RequestContext, IntentType
from src.models.decision import (
    DecisionBlueprint,
    StageRecommendation,
    AlternativePlatform,
)

class PlatformRouter:
    """Enterprise Capability-to-Platform Decision Engine & Orchestration Router."""

    def __init__(self, catalog: Optional[Catalog] = None):
        if catalog is None:
            loader = CatalogLoader()
            self.catalog = loader.load()
        else:
            self.catalog = catalog

        self.rule_evaluator = RuleEvaluator(self.catalog.rules)
        self.scoring_engine = ScoringEngine(self.catalog.platforms)
        self.jev_validator = JevValidator()

    def route(self, request: RequestContext, validate_with_jev: bool = True) -> DecisionBlueprint:
        """Processes an enterprise request and produces a multi-platform execution blueprint."""

        # 1. First attempt to match an Enterprise Architecture Policy / Rule
        matched_rule = self.rule_evaluator.evaluate(request)

        # 2. Compute alternatives & scoring for context
        ranked_alternatives = self.scoring_engine.rank_platforms(request)

        if matched_rule:
            blueprint = self._build_blueprint_from_rule(request, matched_rule, ranked_alternatives)
        else:
            # 3. Fallback to MCDA Scoring Engine if no specific rule matched
            blueprint = self._build_blueprint_from_scoring(request, ranked_alternatives)

        # 4. Optional / Default: Run System One Jev Validation on the Blueprint
        if validate_with_jev:
            blueprint_dict = blueprint.model_dump()
            blueprint.jev_validation = self.jev_validator.validate_blueprint(
                blueprint_dict=blueprint_dict,
                platforms_catalog=self.catalog.platforms,
            )

        return blueprint

    def _build_blueprint_from_rule(
        self,
        request: RequestContext,
        rule,
        alternatives: List[AlternativePlatform],
    ) -> DecisionBlueprint:
        stages: List[StageRecommendation] = []

        for idx, stage_spec in enumerate(rule.stages, start=1):
            platform = self.catalog.get_platform(stage_spec.platform_id)
            platform_name = platform.name if platform else stage_spec.platform_id
            platform_tier = platform.tier if platform else "Enterprise Tier"

            # Retrieve utilized features
            cap = platform.get_capability(stage_spec.capability_id) if platform else None
            features = cap.features if cap else []

            stages.append(
                StageRecommendation(
                    stage_number=idx,
                    stage_name=stage_spec.stage_name,
                    phase=stage_spec.phase,
                    platform_id=stage_spec.platform_id,
                    platform_name=platform_name,
                    platform_tier=platform_tier,
                    capability_id=stage_spec.capability_id,
                    action=stage_spec.action,
                    rationale=stage_spec.rationale,
                    features_utilized=features,
                )
            )

        # Derive recommended integrations if multiple platforms are engaged
        integrations = self._derive_integrations(stages)

        summary = (
            f"Rule '{rule.name}' matched. "
            f"Orchestrates across {len(stages)} lifecycle stages using {len(set(s.platform_id for s in stages))} platform(s)."
        )

        return DecisionBlueprint(
            initiative_name=request.initiative_name or f"{request.domain} - {request.capability}",
            request=request,
            decision_type="rule_matched",
            matched_rule_id=rule.id,
            matched_rule_name=rule.name,
            stages=stages,
            architecture_summary=summary,
            recommended_integrations=integrations,
            alternatives_considered=alternatives,
            metadata={"priority": rule.priority},
        )

    def _build_blueprint_from_scoring(
        self,
        request: RequestContext,
        alternatives: List[AlternativePlatform],
    ) -> DecisionBlueprint:
        stages: List[StageRecommendation] = []

        if alternatives:
            top_choice = alternatives[0]
            platform = self.catalog.get_platform(top_choice.platform_id)
            platform_name = platform.name if platform else top_choice.platform_id
            platform_tier = platform.tier if platform else "Enterprise Tier"

            cap = platform.get_capability(request.capability) if platform else None
            features = cap.features if cap else []

            stages.append(
                StageRecommendation(
                    stage_number=1,
                    stage_name=f"1. Implement {request.capability} on {platform_name}",
                    phase="build_and_deploy",
                    platform_id=top_choice.platform_id,
                    platform_name=platform_name,
                    platform_tier=platform_tier,
                    capability_id=request.capability,
                    action=f"Implement and configure '{request.capability}' capability directly on {platform_name}.",
                    rationale=f"Highest capability match score ({top_choice.score}) based on enterprise catalog features and tier alignment.",
                    features_utilized=features,
                )
            )
            summary = f"No explicit rule matched. Selected '{platform_name}' via capability scoring ({top_choice.score})."
        else:
            summary = "No suitable platform found in enterprise catalog for the requested capability."

        return DecisionBlueprint(
            initiative_name=request.initiative_name or f"{request.domain} - {request.capability}",
            request=request,
            decision_type="capability_scored" if alternatives else "fallback",
            matched_rule_id=None,
            matched_rule_name=None,
            stages=stages,
            architecture_summary=summary,
            recommended_integrations=[],
            alternatives_considered=alternatives,
        )

    def _derive_integrations(self, stages: List[StageRecommendation]) -> List[str]:
        integrations: List[str] = []
        platform_ids = [s.platform_id for s in stages]

        if "green_platform" in platform_ids and "purple_platform" in platform_ids:
            integrations.append(
                "Green Platform <-> Purple Platform: REST Webhooks or Event Broker (Kafka) for async status sync and bidirectional master record updates."
            )

        if "blue_platform" in platform_ids and "purple_platform" in platform_ids:
            integrations.append(
                "Blue Platform <-> Purple Platform: CRM Event Trigger to launch bespoke workflow tasks."
            )

        if "dark_blue_platform" in platform_ids and "green_platform" in platform_ids:
            integrations.append(
                "Green Platform <-> Dark Blue Platform: Secure Payroll Data Exchange (Employee Demographics, Time & Attendance, Tax elections)."
            )

        return integrations
