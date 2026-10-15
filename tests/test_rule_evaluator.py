import pytest
from src.engine.catalog import CatalogLoader
from src.engine.rule_evaluator import RuleEvaluator
from src.models.request import RequestContext, IntentType

def test_rule_matching_optimize_onboarding():
    catalog = CatalogLoader().load()
    evaluator = RuleEvaluator(catalog.rules)

    req = RequestContext(
        domain="HR",
        capability="hr.onboarding",
        intent=IntentType.OPTIMIZE_EXISTING,
    )

    matched = evaluator.evaluate(req)
    assert matched is not None
    assert matched.id == "RULE_HR_OPTIMIZE_EXISTING_ONBOARDING"
    assert len(matched.stages) == 3
    assert matched.stages[0].platform_id == "green_platform"
    assert matched.stages[1].platform_id == "purple_platform"
    assert matched.stages[2].platform_id == "green_platform"

def test_rule_matching_new_onboarding():
    catalog = CatalogLoader().load()
    evaluator = RuleEvaluator(catalog.rules)

    req = RequestContext(
        domain="HR",
        capability="hr.onboarding",
        intent=IntentType.BUILD_NEW,
    )

    matched = evaluator.evaluate(req)
    assert matched is not None
    assert matched.id == "RULE_HR_BUILD_NEW_ONBOARDING"
    assert matched.stages[0].platform_id == "purple_platform"

def test_rule_matching_crm():
    catalog = CatalogLoader().load()
    evaluator = RuleEvaluator(catalog.rules)

    req = RequestContext(
        domain="CRM",
        capability="crm.pipeline",
        intent=IntentType.BUILD_NEW,
    )

    matched = evaluator.evaluate(req)
    assert matched is not None
    assert matched.id == "RULE_CRM_PROCESS"
    assert matched.stages[0].platform_id == "blue_platform"

def test_rule_matching_payroll():
    catalog = CatalogLoader().load()
    evaluator = RuleEvaluator(catalog.rules)

    req = RequestContext(
        domain="FINANCE",
        capability="finance.payroll",
        intent=IntentType.UPDATE_CORE_PROCESS,
    )

    matched = evaluator.evaluate(req)
    assert matched is not None
    assert matched.id == "RULE_PAYROLL_PROCESS"
    assert matched.stages[0].platform_id == "dark_blue_platform"
