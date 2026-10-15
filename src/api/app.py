from typing import List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from src.models.request import RequestContext
from src.models.decision import DecisionBlueprint
from src.models.platform import Platform
from src.models.rule import DecisionRule
from src.engine.router import PlatformRouter
from src.engine.catalog import CatalogLoader

app = FastAPI(
    title="Enterprise Capability-to-Platform Decision Engine API",
    description="Dynamic decision-maker routing business capabilities to optimal enterprise platforms.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

router_engine = PlatformRouter()
catalog_loader = CatalogLoader()

@app.get("/health", tags=["System"])
def health_check():
    return {"status": "ok", "service": "platform-decision-engine"}

@app.post("/decide", response_model=DecisionBlueprint, tags=["Decision Engine"])
def make_decision(request: RequestContext):
    """
    Evaluates an enterprise capability request and returns a multi-stage platform execution blueprint.
    """
    try:
        blueprint = router_engine.route(request)
        return blueprint
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/platforms", response_model=List[Platform], tags=["Catalog"])
def list_platforms():
    """Returns all registered enterprise platforms."""
    catalog = catalog_loader.load()
    return catalog.list_platforms()

@app.get("/platforms/{platform_id}", response_model=Platform, tags=["Catalog"])
def get_platform(platform_id: str):
    """Returns a specific platform by ID."""
    catalog = catalog_loader.load()
    platform = catalog.get_platform(platform_id)
    if not platform:
        raise HTTPException(status_code=404, detail=f"Platform '{platform_id}' not found")
    return platform

@app.get("/rules", response_model=List[DecisionRule], tags=["Rules"])
def list_rules():
    """Returns all active architecture routing rules."""
    catalog = catalog_loader.load()
    return catalog.list_rules()
