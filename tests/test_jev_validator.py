import pytest
from src.engine.jev_validator import JevValidator, JevClient
from src.engine.router import PlatformRouter
from src.models.request import RequestContext, IntentType

def test_jev_validator_local():
    validator = JevValidator()
    router = PlatformRouter()

    req = RequestContext(
        initiative_name="Optimize Onboarding",
        domain="HR",
        capability="hr.onboarding",
        intent=IntentType.OPTIMIZE_EXISTING,
    )

    blueprint = router.route(req, validate_with_jev=True)

    assert blueprint.jev_validation is not None
    assert blueprint.jev_validation.success is True
    assert blueprint.jev_validation.is_valid_architecture.probability >= 0.90
    assert blueprint.jev_validation.is_valid_architecture.verdict is True
    assert blueprint.jev_validation.is_governance_compliant.verdict is True
    assert blueprint.jev_validation.primary_platform_fit.chosen == "purple_platform"
    assert blueprint.jev_validation.architecture_alignment_score.score >= 2.5

def test_jev_validator_crm():
    validator = JevValidator()
    router = PlatformRouter()

    req = RequestContext(
        initiative_name="New CRM Funnel",
        domain="CRM",
        capability="crm.process",
        intent=IntentType.BUILD_NEW,
    )

    blueprint = router.route(req, validate_with_jev=True)
    assert blueprint.jev_validation is not None
    assert blueprint.jev_validation.primary_platform_fit.chosen == "blue_platform"
