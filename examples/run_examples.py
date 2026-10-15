import json
from pathlib import Path
import sys

project_root = str(Path(__file__).resolve().parent.parent)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.models.request import RequestContext
from src.engine.router import PlatformRouter

def main():
    router = PlatformRouter()
    examples_dir = Path(__file__).resolve().parent

    for json_file in sorted(examples_dir.glob("*.json")):
        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        req = RequestContext.model_validate(data)
        blueprint = router.route(req)

        print(f"\n=======================================================")
        print(f"Scenario File: {json_file.name}")
        print(f"Initiative   : {blueprint.initiative_name}")
        print(f"Decision Type: {blueprint.decision_type}")
        print(f"Summary      : {blueprint.architecture_summary}")
        print("Stages:")
        for stage in blueprint.stages:
            print(f"  Stage {stage.stage_number} [{stage.platform_name}]:")
            print(f"    Action   : {stage.action}")
            print(f"    Rationale: {stage.rationale}")
        if blueprint.recommended_integrations:
            print("Integrations:")
            for integ in blueprint.recommended_integrations:
                print(f"  - {integ}")

if __name__ == "__main__":
    main()
