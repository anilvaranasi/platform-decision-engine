import pytest
from src.engine.catalog import CatalogLoader

def test_catalog_loader():
    loader = CatalogLoader()
    catalog = loader.load()

    assert "purple_platform" in catalog.platforms
    assert "green_platform" in catalog.platforms
    assert "blue_platform" in catalog.platforms
    assert "dark_blue_platform" in catalog.platforms

    green = catalog.get_platform("green_platform")
    assert green is not None
    assert green.has_capability("hr.onboarding.process_mining")
    assert green.capability_strength("hr.onboarding.process_mining") == 0.92

    assert len(catalog.rules) >= 4
    # Ensure rules are ordered by priority descending
    priorities = [r.priority for r in catalog.rules]
    assert priorities == sorted(priorities, reverse=True)
