import pytest
from src.engine.router import PlatformRouter
from src.models.request import RequestContext, IntentType

def test_scenario_optimize_hr_onboarding():
    """
    Scenario: User wants to optimize existing HR onboarding.
    Expected: Discovery on Green (Process Mining) -> Build in Purple -> Sync to Green (SoR).
    """
    router = PlatformRouter()
    req = RequestContext(
        initiative_name="Revamp Enterprise Onboarding",
        domain="HR",
        capability="hr.onboarding",
        intent=IntentType.OPTIMIZE_EXISTING,
    )

    blueprint = router.route(req)

    assert blueprint.decision_type == "rule_matched"
    assert blueprint.matched_rule_id == "RULE_HR_OPTIMIZE_EXISTING_ONBOARDING"
    assert len(blueprint.stages) == 3

    # Stage 1: Green Platform (Process Mining)
    assert blueprint.stages[0].platform_id == "green_platform"
    assert "process mining" in blueprint.stages[0].action.lower()

    # Stage 2: Purple Platform (Workflow build)
    assert blueprint.stages[1].platform_id == "purple_platform"
    assert "purple platform" in blueprint.stages[1].platform_name.lower()

    # Stage 3: Green Platform (System of Record Sync)
    assert blueprint.stages[2].platform_id == "green_platform"
    assert len(blueprint.recommended_integrations) > 0


def test_scenario_build_new_hr_onboarding():
    """
    Scenario: User wants to build a brand new onboarding process from scratch.
    Expected: Build on Purple Platform -> Sync to Green Platform.
    """
    router = PlatformRouter()
    req = RequestContext(
        initiative_name="New Hire Digital Portal",
        domain="HR",
        capability="hr.onboarding",
        intent=IntentType.BUILD_NEW,
    )

    blueprint = router.route(req)

    assert blueprint.decision_type == "rule_matched"
    assert blueprint.matched_rule_id == "RULE_HR_BUILD_NEW_ONBOARDING"
    assert blueprint.stages[0].platform_id == "purple_platform"


def test_scenario_new_crm_process():
    """
    Scenario: User wants to build a new CRM process.
    Expected: Routed to Blue Platform.
    """
    router = PlatformRouter()
    req = RequestContext(
        initiative_name="Enterprise Lead Routing",
        domain="CRM",
        capability="crm.process",
        intent=IntentType.BUILD_NEW,
    )

    blueprint = router.route(req)

    assert blueprint.decision_type == "rule_matched"
    assert blueprint.matched_rule_id == "RULE_CRM_PROCESS"
    assert blueprint.stages[0].platform_id == "blue_platform"


def test_scenario_update_payroll_process():
    """
    Scenario: User wants to update statutory payroll process.
    Expected: Routed to Dark Blue Platform.
    """
    router = PlatformRouter()
    req = RequestContext(
        initiative_name="2025 Tax Rule Update",
        domain="FINANCE",
        capability="finance.payroll",
        intent=IntentType.UPDATE_CORE_PROCESS,
    )

    blueprint = router.route(req)

    assert blueprint.decision_type == "rule_matched"
    assert blueprint.matched_rule_id == "RULE_PAYROLL_PROCESS"
    assert blueprint.stages[0].platform_id == "dark_blue_platform"
