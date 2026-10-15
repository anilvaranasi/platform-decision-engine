import os
from pathlib import Path
from typing import Dict, List, Optional
import yaml

from src.models.platform import Platform
from src.models.capability import Domain, Capability
from src.models.rule import DecisionRule

class Catalog:
    def __init__(
        self,
        platforms: Dict[str, Platform],
        domains: Dict[str, Domain],
        rules: List[DecisionRule],
    ):
        self.platforms = platforms
        self.domains = domains
        self.rules = sorted(rules, key=lambda r: r.priority, reverse=True)

    def get_platform(self, platform_id: str) -> Optional[Platform]:
        return self.platforms.get(platform_id)

    def list_platforms(self) -> List[Platform]:
        return list(self.platforms.values())

    def get_domain(self, domain_id: str) -> Optional[Domain]:
        return self.domains.get(domain_id.upper())

    def list_rules(self) -> List[DecisionRule]:
        return self.rules


class CatalogLoader:
    def __init__(self, config_dir: Optional[str] = None):
        if config_dir is None:
            base_dir = Path(__file__).resolve().parent.parent.parent
            self.config_dir = base_dir / "config"
        else:
            self.config_dir = Path(config_dir)

    def load(self) -> Catalog:
        platforms = self._load_platforms()
        domains = self._load_capabilities()
        rules = self._load_rules()
        return Catalog(platforms=platforms, domains=domains, rules=rules)

    def _load_platforms(self) -> Dict[str, Platform]:
        platforms_file = self.config_dir / "platforms.yaml"
        if not platforms_file.exists():
            return {}
        with open(platforms_file, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        
        platforms_map = {}
        for item in data.get("platforms", []):
            platform = Platform.model_validate(item)
            platforms_map[platform.id] = platform
        return platforms_map

    def _load_capabilities(self) -> Dict[str, Domain]:
        caps_file = self.config_dir / "capabilities.yaml"
        if not caps_file.exists():
            return {}
        with open(caps_file, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}

        domains_map = {}
        for item in data.get("domains", []):
            domain = Domain.model_validate(item)
            domains_map[domain.id.upper()] = domain
        return domains_map

    def _load_rules(self) -> List[DecisionRule]:
        rules_file = self.config_dir / "rules.yaml"
        if not rules_file.exists():
            return []
        with open(rules_file, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}

        rules_list = []
        for item in data.get("rules", []):
            rule = DecisionRule.model_validate(item)
            rules_list.append(rule)
        return rules_list
