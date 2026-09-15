# Incremental End-to-End Plan: AI-Assisted Power BI Report Engineering with Groq

## 1. Objective

Build a practical, low-cost, incrementally complex workflow for creating and maintaining stakeholder-ready Power BI reports with AI assistance.

Target architecture:

```text
Excel / CSV / later Jira data
        |
        v
Power BI Project (.pbip)
        |
        +--> Semantic Model
        |
        +--> Power BI Report / PBIR
        |
        v
Power BI Skills + MCP in VS Code
        |
        v
Groq (GPT-OSS models)
        |
        +--> Analyze
        +--> Plan
        +--> Author
        +--> Validate
```

### Constraints

- No Fabric Lakehouse/Warehouse dependency.
- No Fabric capacity requirement.
- Power BI Desktop is the primary development environment.
- Power BI Project (`.pbip`) and PBIR/TMDL artifacts are source-controlled development artifacts.
- Groq is the preferred LLM for cost efficiency.
- Existing Power BI/Fabric skills in VS Code are reused wherever applicable.
- Complexity is introduced only after the previous stage is proven.
- LangGraph is deferred until a real requirement appears.

---

# 2. Target Outcome

The mature workflow should allow a user to provide a requirement such as:

> Create a stakeholder dashboard for Jira defects and highlight the biggest risks.

The AI-assisted workflow should be able to:

1. Inspect the Power BI project.
2. Understand the semantic model.
3. Use existing measures.
4. Create or modify measures when required.
5. Plan report pages and visuals.
6. Create or modify visuals.
7. Validate semantic-model/report changes.
8. Render and review the report.
9. Correct issues.
10. Produce a stakeholder-ready Power BI project.

Later, the same workflow can consume real Jira data and produce recurring intelligence.

---

# 3. Core Architecture Principles

## 3.1 Power BI is the source of truth

Business calculations belong in the semantic model.

Preferred:

```text
Fact data
   |
   v
Semantic Model
   |
   v
DAX measures
   |
   v
Aggregated query result
   |
   v
Groq reasoning
```

Avoid sending the entire fact table to the LLM.

## 3.2 Groq is the reasoning layer

Groq should primarily handle:

- requirement interpretation
- report planning
- business reasoning
- risk/anomaly interpretation
- natural-language explanations
- structured decisions
- tool selection

Power BI should handle:

- calculations
- filtering
- aggregation
- relationships
- business measures
- report rendering

## 3.3 Skills provide domain knowledge; MCP provides live capabilities

Use the existing Power BI skills and MCP capabilities in VS Code rather than recreating equivalent functionality.

## 3.4 Smallest useful architecture first

Start with:

```text
Groq -> Power BI query
```

Then:

```text
Groq -> Power BI query -> reasoning
```

Then:

```text
Groq -> report authoring
```

Then:

```text
Groq -> author -> validate -> visually review -> fix
```

Only later consider multi-agent orchestration.

---

# 4. Initial Test Dataset

Use the generated workbook:

`power_bi_jira_defect_test_data.xlsx`

It contains approximately 1,200 synthetic Jira-style defects plus supporting dimensions and validation data.

| Sheet | Purpose |
|---|---|
| `FactDefects` | Main defect fact table |
| `DimProject` | Project dimension |
| `DimDate` | Date dimension |
| `DimPriority` | Priority/SLA mapping |
| `DimStatus` | Status classification |
| `ExpectedKPIs` | Ground-truth KPI validation |
| `MonthlyTrend` | Trend validation |

Use this dataset until the complete AI-assisted Power BI workflow works reliably.

Do not introduce real Jira integration early.

---

# 5. Phase 0 — Environment Inventory

## Objective

Understand exactly what Power BI skills, MCP servers, VS Code extensions, local tools, and model endpoints are already available.

## Tasks

### 0.1 Inventory VS Code

Confirm:

- Power BI extensions
- Fabric/Power BI skills
- MCP configuration
- Git
- Power BI Desktop
- PBIP/PBIR support
- TMDL support
- Python availability if useful
- Groq API access

### 0.2 Inventory existing skills

Identify capabilities for:

- semantic model inspection
- semantic model authoring
- DAX
- report planning
- report authoring
- report validation
- screenshot/rendering
- report management

Do not install duplicate tooling before checking what already exists.

### 0.3 Repository

Recommended:

```text
jira-defect-powerbi-ai/
|
+-- data/
|   +-- power_bi_jira_defect_test_data.xlsx
|
+-- powerbi/
|   +-- JiraDefectIntelligence.pbip
|   +-- JiraDefectIntelligence.Report/
|   +-- JiraDefectIntelligence.SemanticModel/
|
+-- prompts/
+-- tests/
+-- docs/
+-- .gitignore
```

## Exit criteria

- Power BI Desktop opens.
- Existing Power BI skills are identified.
- MCP requirements are understood.
- Git repository exists.
- Test workbook is available.

---

# 6. Phase 1 — Create the Baseline Power BI Project

## Objective

Create a clean Power BI project without AI automation.

## Tasks

1. Open Power BI Desktop.
2. Import `FactDefects`.
3. Import dimensions.
4. Create a star schema.
5. Create a dedicated Date table.
6. Mark the Date table.
7. Create relationships.
8. Hide technical keys where appropriate.
9. Set correct data types.
10. Configure basic formatting.

Recommended model:

```text
                    DimDate
                       |
                       |
DimProject ---- FactDefects ---- DimPriority
                       |
                       |
                  DimStatus
```

## Initial measures

```DAX
Total Defects =
COUNTROWS(FactDefects)
```

```DAX
Open Defects =
CALCULATE(
    [Total Defects],
    FactDefects[OpenFlag] = 1
)
```

```DAX
Closed Defects =
CALCULATE(
    [Total Defects],
    FactDefects[ClosedFlag] = 1
)
```

```DAX
Highest Priority Defects =
CALCULATE(
    [Total Defects],
    FactDefects[Priority] = "Highest"
)
```

```DAX
High + Highest Defects =
CALCULATE(
    [Total Defects],
    FactDefects[Priority] IN {"Highest", "High"}
)
```

```DAX
SLA Breached =
CALCULATE(
    [Total Defects],
    FactDefects[SLABreached] = "Yes"
)
```

```DAX
Reopened Defects =
CALCULATE(
    [Total Defects],
    FactDefects[Status] = "Reopened"
)
```

```DAX
Average Age =
AVERAGE(FactDefects[AgeDays])
```

## Exit criteria

Power BI values match the `ExpectedKPIs` sheet.

Initial ground truth:

| KPI | Expected |
|---|---:|
| Total defects | 1203 |
| Open defects | 849 |
| Closed/Resolved defects | 354 |
| Highest priority | 137 |
| High priority | 346 |
| Open High/Highest | 357 |
| Open SLA-breached | 813 |
| All SLA-breached | 1097 |
| Reopened | 127 |

Do not proceed until the baseline is correct.

---

# 7. Phase 2 — PBIP and Git Baseline

## Objective

Make the Power BI project an AI-editable, source-controlled and reversible artifact.

## Tasks

1. Save as Power BI Project.
2. Confirm `.pbip`.
3. Confirm report artifacts.
4. Confirm semantic-model artifacts.
5. Add to Git.
6. Commit the known-good baseline.

Suggested commit:

```text
baseline: Jira defect Power BI model and report
```

Never let AI work against the only copy.

## Exit criteria

A clean Git checkout reproduces the baseline.

---

# 8. Phase 3 — Build the Stakeholder Report

Create the baseline report before introducing autonomous AI changes.

## Page 1 — Executive Overview

KPIs:

- Total Defects
- Open Defects
- High + Highest
- SLA Breached
- Reopened
- Average Age

Visuals:

- Monthly defect trend
- Defects by priority
- Defects by status
- Defects by project
- SLA breach overview

## Page 2 — Defect Analysis

- Priority x Status
- Aging buckets
- Component
- Assignee
- Environment
- Customer impact
- Monthly trend

## Page 3 — Risk Analysis

- Oldest High/Highest defects
- SLA breach by project
- SLA breach by component
- Reopened defects by component
- High-risk project comparison

## Page 4 — Details

Table:

- IssueKey
- Summary
- Project
- Priority
- Status
- Component
- Assignee
- Age
- SLA
- Customer Impact

Add drill-through where useful.

## Exit criteria

A stakeholder can use the report without AI.

This is the baseline against which AI changes are judged.

---

# 9. Phase 4 — Make the Semantic Model AI-Friendly

## Objective

Improve model metadata so the AI agent can understand business meaning.

For important measures add:

- description
- business definition
- correct format
- meaningful name

Example:

```text
Measure:
Open Defects

Description:
Number of defects currently in Open, In Progress,
or Reopened status.
```

Add useful synonyms:

| Business term | Model term |
|---|---|
| Critical | Highest |
| Critical defects | Highest Priority Defects |
| High priority | High |
| Active defects | Open Defects |
| SLA violations | SLA Breached |
| Reopened bugs | Reopened Defects |

Hide technical fields that should not be used directly by report consumers.

## Exit criteria

A person unfamiliar with the model can understand the major tables and measures from metadata.

---

# 10. Phase 5 — First Groq Proof of Concept

## Objective

Prove Groq connectivity independently of Power BI.

## Model strategy

### GPT-OSS 20B

Use for:

- routing
- simple classification
- formatting
- lightweight reasoning

### GPT-OSS 120B

Use for:

- complex reasoning
- report planning
- semantic-model reasoning
- final stakeholder insights

## First test

Send five KPI values to Groq and request structured JSON:

```json
{
  "risk_level": "HIGH",
  "top_risks": [],
  "recommended_actions": []
}
```

## Exit criteria

- Groq API works.
- Structured output works.
- Model routing works.
- 20B and 120B can be selected deliberately.

---

# 11. Phase 6 — Connect Groq to Power BI Through Existing MCP/Skills

## Objective

Allow the LLM to obtain live information from the semantic model.

Do not modify the report yet.

Workflow:

```text
User question
      |
      v
Groq
      |
      v
Inspect semantic model
      |
      v
Generate/query DAX
      |
      v
Power BI
      |
      v
Small structured result
      |
      v
Groq
      |
      v
Answer
```

Test:

1. How many defects are currently open?
2. How many High/Highest defects are open?
3. Which project has the most open defects?
4. Which component has the highest SLA breach count?
5. How many defects were reopened?

## Cost rule

Never send the whole fact table to Groq.

Preferred:

```text
Power BI -> 5-row aggregation -> Groq
```

not:

```text
1203 records -> Groq
```

## Exit criteria

Natural-language questions can be answered from live semantic-model data.

---

# 12. Phase 7 — Controlled Power BI Analyst Agent

## Objective

Move from isolated questions to a reusable analytical workflow.

Agent/persona:

```text
Power BI Defect Analyst
```

Responsibilities:

1. Understand the question.
2. Inspect model metadata when necessary.
3. Prefer existing measures.
4. Generate DAX only when necessary.
5. Query Power BI.
6. Analyze the result.
7. Return concise business reasoning.

Important instruction:

> Prefer existing semantic-model measures over recreating business logic.

## Exit criteria

The agent reliably answers a useful set of stakeholder questions.

---

# 13. Phase 8 — Risk Intelligence

## Objective

Make Groq useful for interpretation, not calculation.

Workflow:

```text
Power BI
   |
   +-- Open defects by project
   +-- SLA breaches by project
   +-- Average age
   +-- High/Critical backlog
   +-- Reopened trend
   |
   v
Groq
   |
   v
Risk assessment
```

Recommended output:

```json
{
  "overall_risk": "HIGH",
  "risks": [
    {
      "title": "...",
      "severity": "HIGH",
      "evidence": ["..."],
      "recommended_action": "..."
    }
  ]
}
```

Every risk must be supported by Power BI evidence.

Avoid:

> The team has a productivity problem.

Prefer:

> OMEN-DE has 281 open defects and 244 SLA breaches, making it the highest current backlog risk.

## Exit criteria

AI-generated insights are traceable to semantic-model results.

---

# 14. Phase 9 — Introduce Power BI Report Planning

## Objective

Make AI plan report changes before authoring them.

Workflow:

```text
Requirement
    |
    v
Report Planner
    |
    v
Report brief
    |
    v
Approval
    |
    v
Authoring
```

Example requirement:

> Add a stakeholder view showing SLA risk by component.

Expected plan:

```text
Page:
Risk Analysis

Visual:
Bar chart

Category:
Component

Value:
SLA Breached

Sort:
Descending

Purpose:
Identify components generating the largest SLA backlog.
```

## Exit criteria

AI produces a clear implementation plan before modifying PBIR.

---

# 15. Phase 10 — First AI Report Modification

## Objective

Make one controlled report change.

Example:

> Add a visual showing SLA breaches by component.

Workflow:

```text
User
 |
 v
Groq
 |
 v
Inspect model
 |
 v
Inspect current report
 |
 v
Plan visual
 |
 v
Report Authoring skill
 |
 v
PBIR modification
 |
 v
Validation
```

Start with one visual.

Do not begin with full-page redesigns.

## Exit criteria

AI successfully creates one correct visual without damaging existing content.

---

# 16. Phase 11 — Structural Validation

After every AI modification:

```text
Modify
  |
  v
Validate
  |
  +--> PASS
  |
  +--> FAIL -> Diagnose -> Fix
```

Validate:

- report structure
- pages
- visuals
- visual configuration
- measure references
- field references
- filters
- relationships
- invalid references

## Exit criteria

No AI report change is considered complete until validation passes.

---

# 17. Phase 12 — Screenshot/Visual QA

Structural validation is not enough.

Workflow:

```text
PBIR modification
       |
       v
Structural validation
       |
       v
Render/open Power BI
       |
       v
Screenshot
       |
       v
AI visual review
       |
       +--> PASS
       |
       +--> FAIL -> Modify -> Render again
```

Check:

- overlapping visuals
- unreadable labels
- clipped titles
- excessive whitespace
- inconsistent alignment
- poor chart selection
- confusing slicers
- excessive density
- weak visual hierarchy

## Exit criteria

AI-generated changes are structurally valid and visually acceptable.

---

# 18. Phase 13 — Automated KPI Regression Testing

Use `ExpectedKPIs` as the first regression-test suite.

Example:

```text
Metric                         Expected
------------------------------------------------
Total Defects                  1203
Open Defects                    849
Closed/Resolved                 354
Highest                         137
High                            346
Open High/Highest               357
Open SLA Breached               813
All SLA Breached               1097
Reopened                        127
```

Return structured results:

```json
{
  "status": "PASS",
  "tests": [
    {
      "metric": "Open Defects",
      "expected": 849,
      "actual": 849,
      "status": "PASS"
    }
  ]
}
```

## Exit criteria

The workflow can automatically determine whether a report/model change preserved core KPIs.

---

# 19. Phase 14 — Closed-Loop Power BI Builder

Combine planning, authoring, structural validation, KPI tests and visual QA.

```text
Requirement
    |
    v
Understand
    |
    v
Inspect semantic model
    |
    v
Inspect report
    |
    v
Plan
    |
    v
Author
    |
    v
Structural validation
    |
    v
KPI regression
    |
    v
Render
    |
    v
Visual QA
    |
    +---- FAIL ----> Fix
    |
    v
PASS
```

This is the first genuinely agentic version.

---

# 20. Phase 15 — Human Approval Gates

Use approval based on change risk.

## Low risk — may auto-execute

- Add simple visual
- Change visual title
- Add slicer
- Adjust label formatting

## Medium risk — approval recommended

- Create/change measures
- Modify relationships
- Significant page layout changes

## High risk — mandatory approval

- Delete pages
- Delete measures
- Change business logic
- Change data source
- Change security/RLS
- Mass visual modifications

Pattern:

```text
AI proposes
     |
     v
Risk classification
     |
     +--> LOW -> execute
     |
     +--> MEDIUM -> approval
     |
     +--> HIGH -> mandatory approval
```

---

# 21. Phase 16 — Optimize Groq Cost

## Rule 1 — Query, don't dump

Reduce Power BI data before sending it to Groq.

## Rule 2 — Cache metadata

Cache:

- tables
- columns
- measures
- relationships
- descriptions

Avoid rediscovering the schema every time.

## Rule 3 — Reuse measures

Prefer existing semantic-model measures.

## Rule 4 — Use 20B by default

Route to 120B only for tasks that genuinely need stronger reasoning.

## Rule 5 — Structured outputs

Use compact JSON for machine-to-machine communication.

## Rule 6 — Minimal context

Send only the model metadata and query result required for the current task.

## Rule 7 — Modular prompts

Prefer:

```text
system instructions
+
task
+
minimal model context
+
query result
```

rather than injecting the whole project description every time.

---

# 22. Phase 17 — Introduce Real Jira Data

Only after the test-data workflow is reliable.

New architecture:

```text
Jira
 |
 v
Export/API/Connector
 |
 v
Power BI
 |
 v
Semantic Model
 |
 v
Report
 |
 v
AI Agent
```

The report should remain largely independent of the ingestion mechanism.

Goal:

```text
test-data.xlsx
       |
       v
real Jira data
```

without redesigning the semantic model/report unnecessarily.

---

# 23. Phase 18 — Refresh and Recurring Intelligence

Once real data is available:

```text
Data refresh
     |
     v
Power BI semantic model
     |
     v
Regression tests
     |
     v
AI analysis
     |
     v
Change/risk detection
     |
     v
Stakeholder summary
```

Example:

```text
Daily Defect Intelligence

Overall Risk: HIGH

Changes since yesterday:
- Open critical defects: +7
- SLA breaches: +31
- Reopened defects: +8

Largest concern:
OMEN-DE
```

Notify stakeholders only when changes are meaningful.

---

# 24. Phase 19 — Reassess LangGraph

Do not add LangGraph merely because the solution is agentic.

Reconsider only if the workflow needs:

- persistent state
- complex branching
- long-running jobs
- multiple specialized agents
- advanced retry/recovery
- durable approval workflows
- complex parallel execution

Until then:

```text
One agent
+
Tools
+
Skills
+
Structured workflow
```

is preferred.

---

# 25. Recommended Agent Roles

Initially use one agent with task modes:

```text
Power BI Assistant
|
+-- Analyst mode
|
+-- Planner mode
|
+-- Builder mode
|
+-- Reviewer mode
```

Do not create four separate LLM agents initially.

---

# 26. Power BI Skill Usage

Use existing skills according to the task.

| Task | Preferred capability |
|---|---|
| Understand model | Semantic model skill |
| Create/change measures | Semantic model authoring |
| Plan report | Report Planner |
| Create/change visuals | Report Authoring |
| Validate report | Report validation |
| Inspect live model | Power BI MCP |
| Understand requirement | Groq |
| Explain results | Groq |
| Visual QA | Groq + rendered report |
| Regression testing | Deterministic validation |

Principle:

> Use a Power BI skill whenever the task is fundamentally a Power BI operation; use Groq for interpretation and decision-making.

---

# 27. Prompt Architecture

Do not create one enormous system prompt.

Use modular instructions.

## Base

```text
You are a Power BI engineering assistant.

Power BI is the source of truth for calculations.
Use existing semantic-model measures whenever possible.
Do not calculate business KPIs from raw data when Power BI can calculate them.
Use available Power BI skills and MCP tools instead of recreating their functionality.
Never modify the report without inspecting the current state.
After modifications, validate the report.
Prefer the smallest safe change.
```

## Analyst

```text
Answer business questions using the Power BI semantic model.
Generate the smallest necessary query.
Return only the data required for reasoning.
Explain conclusions using evidence from the query result.
```

## Builder

```text
Before modifying the report:
1. Inspect the semantic model.
2. Inspect the current report.
3. Produce a concise implementation plan.
4. Make the smallest required change.
5. Validate the result.
6. Do not delete or replace existing content unless explicitly requested.
```

## Reviewer

```text
Review the report for:
1. correctness
2. usability
3. visual hierarchy
4. layout
5. business relevance
6. KPI consistency

Return PASS or FAIL with specific evidence.
```

---

# 28. Git and Recovery

Every meaningful AI change should be reversible.

Recommended branches:

```text
main
 |
 +-- baseline
 |
 +-- ai/change-sla-component
 |
 +-- ai/change-risk-page
 |
 +-- ai/layout-improvement
```

Before AI modification:

```bash
git status
git add .
git commit -m "checkpoint before AI change"
```

After successful validation:

```bash
git commit -m "AI: add SLA breach by component visual"
```

If an AI change is bad, use Git to inspect/revert it.

Do not rely on the LLM to remember how to undo its own changes.

---

# 29. MVP Definition of Done

## Data

- [ ] Test workbook loads.
- [ ] Star schema is correct.
- [ ] Date dimension works.

## Semantic model

- [ ] Core measures exist.
- [ ] KPI values match expected values.
- [ ] Measures have useful descriptions.
- [ ] Technical fields are appropriately hidden.

## Report

- [ ] Four stakeholder pages exist.
- [ ] Filters work.
- [ ] Drill-through works where appropriate.
- [ ] Report is visually acceptable.

## AI

- [ ] Groq 20B works.
- [ ] Groq 120B works.
- [ ] Natural-language questions query Power BI.
- [ ] AI explains KPI results.
- [ ] AI identifies risks.

## Authoring

- [ ] AI can plan a report change.
- [ ] AI can create one visual.
- [ ] AI can modify one existing visual.
- [ ] Structural validation works.
- [ ] KPI regression tests work.
- [ ] Screenshot/visual QA works.

## Safety

- [ ] Git baseline exists.
- [ ] AI changes are reversible.
- [ ] High-risk changes require approval.

---

# 30. Exact Implementation Sequence

```text
STEP 01
Inventory existing VS Code Power BI skills
        |
STEP 02
Create Git repository
        |
STEP 03
Import test Excel into Power BI
        |
STEP 04
Create PBIP
        |
STEP 05
Build semantic model
        |
STEP 06
Create DAX measures
        |
STEP 07
Validate ExpectedKPIs
        |
STEP 08
Create stakeholder report
        |
STEP 09
Improve semantic-model descriptions
        |
STEP 10
Connect Groq
        |
STEP 11
Connect Groq -> Power BI MCP
        |
STEP 12
Answer live semantic-model questions
        |
STEP 13
Add AI risk analysis
        |
STEP 14
Use Report Planner
        |
STEP 15
AI creates one visual
        |
STEP 16
Structural validation
        |
STEP 17
KPI regression testing
        |
STEP 18
Screenshot/visual QA
        |
STEP 19
Closed-loop report authoring
        |
STEP 20
Human approval gates
        |
STEP 21
Optimize token/model routing
        |
STEP 22
Replace test data with Jira data
        |
STEP 23
Add recurring intelligence
        |
STEP 24
Reassess need for LangGraph
```

---

# 31. Milestone-Based Complexity

## Level 1 — Deterministic Power BI

```text
Excel
 -> Power BI
 -> Semantic Model
 -> Report
```

Goal: trustworthy baseline.

## Level 2 — AI Analyst

```text
User
 -> Groq
 -> Power BI MCP
 -> Semantic Model
 -> Groq
 -> Answer
```

Goal: AI can understand live report data.

## Level 3 — AI Planner

```text
Requirement
 -> Groq
 -> Power BI Planner
 -> Plan
```

Goal: AI understands how to implement report changes.

## Level 4 — AI Builder

```text
Plan
 -> PBIR
 -> Validation
```

Goal: AI can safely modify reports.

## Level 5 — Closed Loop

```text
Plan
 -> Build
 -> Validate
 -> Render
 -> Review
 -> Fix
```

Goal: autonomous report engineering.

## Level 6 — Production Intelligence

```text
Jira
 -> Power BI
 -> AI analysis
 -> Change detection
 -> Stakeholder insight
```

Goal: recurring business automation.

## Level 7 — Advanced Orchestration

Only if required:

```text
Multiple agents
State
Retries
Approvals
Parallel tasks
Long-running workflows
```

Potentially introduce LangGraph here.

---

# 32. First Sprint

Do only:

1. Inventory existing VS Code skills.
2. Create Git repository.
3. Import test workbook into Power BI.
4. Create PBIP.
5. Build semantic model.
6. Create core DAX measures.
7. Validate against `ExpectedKPIs`.
8. Create the four-page stakeholder report.
9. Commit a clean baseline.

### Sprint 1 success condition

The report remains useful even if AI is completely removed.

---

# 33. Second Sprint

Then:

1. Configure Groq.
2. Test GPT-OSS 20B.
3. Test GPT-OSS 120B.
4. Connect Power BI MCP.
5. Inspect semantic model through the agent.
6. Execute a simple DAX query.
7. Return the result to Groq.
8. Answer five predefined business questions.

### Sprint 2 success condition

```text
User:
Which project has the highest SLA risk?

Agent:
Queries Power BI
        |
        v
Receives aggregate results
        |
        v
Groq reasons
        |
        v
Evidence-backed answer
```

---

# 34. Third Sprint

Then:

1. Add report planning.
2. Ask AI to propose one visual.
3. Review the plan.
4. Let AI create the visual.
5. Validate PBIR.
6. Render.
7. Visually inspect.
8. Commit.

### Sprint 3 success condition

AI successfully adds a useful visual without breaking the report.

---

# 35. Fourth Sprint

Then:

1. Add automated KPI regression.
2. Add visual QA.
3. Add retry/fix loop.
4. Add approval gates.
5. Add model routing.
6. Measure token usage.

### Sprint 4 success condition

```text
Requirement
 -> Plan
 -> Build
 -> Test
 -> Review
 -> Fix
 -> PASS
```

At this point the project is a credible agentic Power BI engineering prototype.

---

# 36. Final Vision

```text
User:

"Create a stakeholder-ready Power BI view showing
where our Jira defect risks are increasing."

             |
             v

        Groq Agent
             |
             +---- Inspect semantic model
             |
             +---- Inspect report
             |
             +---- Query Power BI
             |
             +---- Analyze results
             |
             +---- Plan changes
             |
             +---- Modify PBIR
             |
             +---- Validate
             |
             +---- Run KPI tests
             |
             +---- Render
             |
             +---- Review screenshot
             |
             +---- Fix if required
             |
             v

      Stakeholder-ready
       Power BI Project
```

## Final architectural rule

> Let Power BI do Power BI work. Let Groq do reasoning. Let the existing Power BI skills/MCP provide controlled capabilities. Keep the data in Power BI and send only the minimum required information to the LLM.

This is the simplest path from a static test report to a genuinely useful AI-assisted Power BI engineering workflow without requiring Fabric infrastructure.
