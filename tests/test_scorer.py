import pytest
from src.engine.catalog import CatalogLoader
from src.engine.scorer import ScoringEngine
from src.models.request import RequestContext, IntentType

def test_scoring_capability():
    catalog = CatalogLoader().load()
    scorer = ScoringEngine(catalog.platforms)

    req = RequestContext(
        domain="CRM",
        capability="crm.process",
        intent=IntentType.BUILD_NEW,
    )

    ranked = scorer.rank_platforms(req)
    assert len(ranked) > 0
    assert ranked[0].platform_id == "blue_platform"
    assert ranked[0].score >= 0.95

def test_scoring_with_features():
    catalog = CatalogLoader().load()
    scorer = ScoringEngine(catalog.platforms)

    purple = catalog.get_platform("purple_platform")
    score, matched = scorer.score_platform_for_capability(
        platform=purple,
        capability_id="hr.onboarding.workflow",
        required_features=["drag_and_drop_forms", "e_signature"],
    )

    assert score > 0.8
    assert "drag_and_drop_forms" in matched
    assert "e_signature" in matched
