# 📌 Executive Summary: Platform Decision Engine (PDE)

**Document Reference:** [`docs/ARCHITECTURE_ARTICLE.md`](docs/ARCHITECTURE_ARTICLE.md)  
**Project:** Enterprise Platform Decision Engine (`platform-decision-engine`)  
**Status:** Approved / Active Reference Architecture  

---

## 1. The Challenge
Enterprises struggle with fragmented platform choices:
- **Monolithic Anti-Pattern:** Teams build bespoke frontends directly inside rigid legacy Systems of Record (e.g. Core HR), causing high maintenance costs and UI rigidity.
- **Data Sprawl:** Teams build ad-hoc apps without syncing back to the authoritative System of Record, creating compliance risks.
- **Disjointed Modernization:** Redesigning flows without data-backed discovery or process mining.

---

## 2. The Solution: Dual-Pass Decision Framework
The **Platform Decision Engine (PDE)** provides an automated, policy-driven framework that routes business capabilities to target platforms and outputs **multi-stage execution blueprints**:

```
[Business Request] 
       │
       ▼
┌───────────────────────────────────────────────┐
│ Pass 1: Deterministic Engine                  │
│ • Match prioritized EA rules (rules.yaml)     │
│ • Decompose into multi-stage lifecycle        │
│ • Fallback to MCDA Scoring (platforms.yaml)   │
└──────────────────────┬────────────────────────┘
                       │ Candidate Blueprint
                       ▼
┌───────────────────────────────────────────────┐
│ Pass 2: TypeSafe Jev System One Validation    │
│ • Sends platform catalog & stages in state    │
│ • Evaluates Noul (soundness & governance)     │
│ • Evaluates Choice (primary platform fit)     │
│ • Evaluates Score (architecture maturity)     │
└──────────────────────┬────────────────────────┘
                       │ Certified Blueprint
                       ▼
 [Stage 1: Discover] ➔ [Stage 2: Build] ➔ [Stage 3: Sync]
```

---

## 3. Platform Architecture Archetypes & Routing Matrix

| Platform | Architectural Role | Benchmark Capability |
| :--- | :--- | :--- |
| **Purple Platform** | **System of Engagement & Orchestration** (Low-Code/DPA) | High-agility UI, onboarding portals, dynamic forms, approval workflows. |
| **Green Platform** | **System of Record & Intelligence** (Core HRIS) | Authoritative employee master data, event log telemetry, embedded Process Mining. |
| **Blue Platform** | **Domain System of Record & Engagement** (CRM) | Sales pipeline, opportunity stages, customer accounts, lead lifecycle. |
| **Dark Blue Platform** | **System of Record** (Payroll & Compliance) | Gross-to-net tax rules, statutory payroll runs, direct deposit disbursements. |

---

## 4. Benchmark Scenario Blueprints

1. **Optimize Existing HR Onboarding (`HR` + `optimize_existing`)**:
   - **Stage 1 (Discovery):** Process Mining on **Green Platform** to uncover bottlenecks.
   - **Stage 2 (Build):** Re-engineered onboarding journey & portal on **Purple Platform**.
   - **Stage 3 (Sync):** Master employee record ingestion back to **Green Platform** (Kafka/Webhooks).
   - **Jev Verdict:** *90% Soundness, 94% Governance, 100% Purple Platform Fit, 2.99 / 3.0 Maturity.*

2. **New HR Onboarding (`HR` + `build_new`)**:
   - Modern portal on **Purple Platform** $\rightarrow$ Automated sync to **Green Platform**.

3. **New CRM Process (`CRM` + `build_new`)**:
   - Direct execution in **Blue Platform**.

4. **Update Payroll Rules (`FINANCE` + `update_core_process`)**:
   - Direct statutory updates in **Dark Blue Platform**.

---

## 5. Developer & Operational Tooling
- **Interactive CLI:** `python src/cli.py demo` or `python src/cli.py decide --domain HR --capability hr.onboarding --intent optimize_existing`
- **Local REST API / Swagger UI:** `http://localhost:8000/docs` (`POST /decide`)
- **Automated Pytest Suite:** 16 tests passing (`python -m pytest -v`)
- **Declarative GitOps Config:** [`config/platforms.yaml`](config/platforms.yaml), [`config/capabilities.yaml`](config/capabilities.yaml), [`config/rules.yaml`](config/rules.yaml)
