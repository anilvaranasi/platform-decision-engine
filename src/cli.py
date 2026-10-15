import os
import sys
from pathlib import Path
from typing import List, Optional

# Ensure project root is in sys.path when invoked directly as a script
project_root = str(Path(__file__).resolve().parent.parent)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.tree import Tree
from rich import print as rprint

from src.models.request import RequestContext, IntentType
from src.engine.router import PlatformRouter
from src.engine.catalog import CatalogLoader

app = typer.Typer(
    name="platform-decision-engine",
    help="Enterprise Capability-to-Platform Decision Engine CLI",
    add_completion=False,
)
console = Console()

@app.command()
def decide(
    domain: str = typer.Option(..., "--domain", "-d", help="Domain e.g. HR, CRM, FINANCE, WORKFLOW"),
    capability: str = typer.Option(..., "--capability", "-c", help="Capability e.g. hr.onboarding, crm.process, finance.payroll"),
    intent: IntentType = typer.Option(IntentType.BUILD_NEW, "--intent", "-i", help="Strategic intent: build_new | optimize_existing | update_core_process"),
    initiative: Optional[str] = typer.Option(None, "--name", "-n", help="Initiative Name"),
    features: Optional[List[str]] = typer.Option(None, "--feature", "-f", help="Specific required features"),
    validate_jev: bool = typer.Option(True, "--validate-jev/--no-validate-jev", "-j", help="Run TypeSafe Jev System One verification"),
):
    """Evaluate and decide platform routing for an enterprise capability requirement."""
    router = PlatformRouter()
    req = RequestContext(
        initiative_name=initiative or f"{domain} - {capability}",
        domain=domain,
        capability=capability,
        intent=intent,
        required_features=features or [],
    )

    blueprint = router.route(req, validate_with_jev=validate_jev)
    _display_blueprint(blueprint)

@app.command()
def list_platforms():
    """List all registered enterprise platforms and their capabilities."""
    loader = CatalogLoader()
    catalog = loader.load()

    table = Table(title="Enterprise Platform Catalog", show_header=True, header_style="bold magenta")
    table.add_column("Platform ID", style="cyan", width=18)
    table.add_column("Name", style="bold", width=22)
    table.add_column("Architecture Tier", style="green", width=32)
    table.add_column("Supported Capabilities", style="yellow")

    for p in catalog.list_platforms():
        caps_str = "\n".join([f"• {c.capability_id} (Score: {c.strength})" for c in p.capabilities])
        table.add_row(p.id, p.name, p.tier, caps_str)

    console.print(table)

@app.command()
def list_rules():
    """List all enterprise architecture decision rules."""
    loader = CatalogLoader()
    catalog = loader.load()

    table = Table(title="Enterprise Architecture Decision Rules", show_header=True, header_style="bold cyan")
    table.add_column("Priority", style="bold yellow", width=10)
    table.add_column("Rule ID / Name", style="bold", width=32)
    table.add_column("Conditions", style="green", width=28)
    table.add_column("Target Stages", style="magenta")

    for r in catalog.list_rules():
        cond_str = f"Domain: {r.conditions.domain or '*'}\nCap: {r.conditions.capability or r.conditions.capability_pattern or '*'}\nIntent: {r.conditions.intent or '*'}"
        stages_str = " -> ".join([s.platform_id for s in r.stages])
        table.add_row(str(r.priority), f"{r.id}\n{r.name}", cond_str, stages_str)

    console.print(table)

@app.command()
def demo():
    """Run all primary enterprise scenarios to showcase dynamic routing."""
    router = PlatformRouter()

    scenarios = [
        RequestContext(
            initiative_name="Optimize Existing HR Onboarding",
            domain="HR",
            capability="hr.onboarding",
            intent=IntentType.OPTIMIZE_EXISTING,
        ),
        RequestContext(
            initiative_name="Build Brand New Employee Onboarding",
            domain="HR",
            capability="hr.onboarding",
            intent=IntentType.BUILD_NEW,
        ),
        RequestContext(
            initiative_name="New CRM Opportunity Pipeline Process",
            domain="CRM",
            capability="crm.process",
            intent=IntentType.BUILD_NEW,
        ),
        RequestContext(
            initiative_name="Update Statutory Payroll Engine Rules",
            domain="FINANCE",
            capability="finance.payroll",
            intent=IntentType.UPDATE_CORE_PROCESS,
        ),
    ]

    for req in scenarios:
        blueprint = router.route(req)
        _display_blueprint(blueprint)
        console.print("\n" + "="*80 + "\n")

def _display_blueprint(blueprint):
    title = f"Decision Blueprint: {blueprint.initiative_name}"
    console.print(Panel(f"[bold cyan]{title}[/bold cyan]\n[italic]{blueprint.architecture_summary}[/italic]", border_style="cyan"))

    # Stage Plan Table
    table = Table(title="Multi-Stage Orchestration Blueprint", show_header=True, header_style="bold blue", expand=True)
    table.add_column("#", style="bold yellow", justify="center", no_wrap=True)
    table.add_column("Stage & Phase", style="bold cyan")
    table.add_column("Platform", style="magenta")
    table.add_column("Action & Strategy", style="white")

    for s in blueprint.stages:
        action_text = f"[bold]Action:[/bold] {s.action}\n[italic green]Rationale:[/italic green] {s.rationale}"
        if s.features_utilized:
            action_text += f"\n[dim]Features: {', '.join(s.features_utilized[:4])}[/dim]"
        table.add_row(str(s.stage_number), f"{s.stage_name}\n[dim]({s.phase})[/dim]", f"{s.platform_name}\n[dim]{s.platform_tier}[/dim]", action_text)

    console.print(table)

    # Integrations
    if blueprint.recommended_integrations:
        tree = Tree("[bold green]Recommended Integrations & Event Flows[/bold green]")
        for integ in blueprint.recommended_integrations:
            tree.add(f"[yellow]{integ}[/yellow]")
        console.print(tree)

    # Jev System One Verification Verdict
    if blueprint.jev_validation:
        jv = blueprint.jev_validation
        jev_status = "[bold green]PASS[/bold green]" if (jv.is_valid_architecture.verdict and jv.is_governance_compliant.verdict) else "[bold red]FAIL[/bold red]"
        
        jev_table = Table(title=f"TypeSafe Jev (System One) Validation [{jev_status}]", show_header=True, header_style="bold green")
        jev_table.add_column("Judgment Dimension", style="cyan")
        jev_table.add_column("TypeSafe Primitive", style="magenta")
        jev_table.add_column("Score / Probability", style="yellow")
        jev_table.add_column("Verdict", style="white")

        jev_table.add_row(
            "Architecture Soundness",
            "Noul (Probability)",
            f"{jv.is_valid_architecture.probability * 100:.1f}%",
            "[green]Compliant[/green]" if jv.is_valid_architecture.verdict else "[red]Risk[/red]"
        )
        jev_table.add_row(
            "Data Governance & Sovereignty",
            "Noul (Probability)",
            f"{jv.is_governance_compliant.probability * 100:.1f}%",
            "[green]Compliant[/green]" if jv.is_governance_compliant.verdict else "[red]Risk[/red]"
        )
        jev_table.add_row(
            "Primary Platform Fit",
            "Choice",
            f"Confidence: {jv.primary_platform_fit.confidence * 100:.1f}%",
            f"[bold cyan]{jv.primary_platform_fit.chosen}[/bold cyan]"
        )
        jev_table.add_row(
            "Maturity & Alignment Level",
            "Score (0–3 Scale)",
            f"{jv.architecture_alignment_score.score:.2f} / 3.0",
            f"Confidence: {jv.architecture_alignment_score.confidence * 100:.1f}%"
        )
        console.print(jev_table)

if __name__ == "__main__":
    app()
