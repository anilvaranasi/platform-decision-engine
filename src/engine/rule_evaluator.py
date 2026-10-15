import re
from typing import List, Optional, Tuple
from src.models.rule import DecisionRule
from src.models.request import RequestContext

class RuleEvaluator:
    """Evaluates enterprise architecture rules and decomposition patterns against requests."""

    def __init__(self, rules: List[DecisionRule]):
        self.rules = sorted(rules, key=lambda r: r.priority, reverse=True)

    def evaluate(self, request: RequestContext) -> Optional[DecisionRule]:
        """Returns the highest priority matching DecisionRule, or None if no rule matches."""
        for rule in self.rules:
            if self._matches(rule, request):
                return rule
        return None

    def _matches(self, rule: DecisionRule, request: RequestContext) -> bool:
        cond = rule.conditions

        # 1. Domain match (case-insensitive)
        if cond.domain:
            if cond.domain.strip().upper() != request.domain.strip().upper():
                return False

        # 2. Intent match
        if cond.intent:
            if cond.intent.strip().lower() != request.intent.value.strip().lower():
                return False

        # 3. Exact Capability match
        if cond.capability:
            req_cap = request.capability.strip().lower()
            rule_cap = cond.capability.strip().lower()
            if req_cap != rule_cap and not req_cap.startswith(rule_cap):
                return False

        # 4. Regex Pattern Capability match
        if cond.capability_pattern:
            req_cap = request.capability.strip().lower()
            pattern = cond.capability_pattern.strip().lower()
            if not re.search(pattern, req_cap):
                return False

        return True
