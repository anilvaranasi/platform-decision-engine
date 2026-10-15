"""Main Entrypoint for Platform Decision Engine (CLI & Web API)."""

import sys
from pathlib import Path

project_root = str(Path(__file__).resolve().parent.parent)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.api.app import app
from src.cli import app as cli_app

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "serve":
        import uvicorn
        port = int(sys.argv[2]) if len(sys.argv) > 2 else 8000
        uvicorn.run("src.main:app", host="0.0.0.0", port=port, reload=True)
    else:
        cli_app()
