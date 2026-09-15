# AI-Driven Power BI Report Generator — Incremental End-to-End Plan

## Version 3 — Reusable AI-first architecture

### Objective

Build a reusable, low-cost AI workflow where the user provides data and business intent, and the system uses **Groq + existing Power BI Skills in VS Code** to inspect, plan, build, validate, and repair a Power BI project.

The system must eventually support:

```text
User provides data + business intent
                |
                v
        AI inspects the data
                |
                v
        AI understands domain
                |
                v
        AI plans semantic model
                |
                v
        Power BI Skills execute
                |
                v
        AI plans KPIs/report
                |
                v
        Power BI Skills build
                |
                v
             Validate
                |
          +-----+-----+
          |           |
        PASS         FAIL
          |           |
          v           v
         Done      AI diagnoses
                       |
                       v
                  Repair/retry
```

The goal is **not** to manually prepare every new project.

The goal is:

> **Give the system data and requirements; let the model determine what needs to be built and use Power BI Skills to perform the work.**

---

# 1. Architecture Principles

## 1.1 No LangGraph in this iteration

Do not introduce LangGraph or another agent framework.

Use a simple Python orchestrator.

The workflow can be implemented as:

```text
PLAN
  ↓
EXECUTE
  ↓
OBSERVE
  ↓
VALIDATE
  ↓
REPAIR if necessary
  ↓
VALIDATE
```

This is already enough to create an agentic workflow.

---

## 1.2 No Fabric dependency

We do not have Fabric licenses.

Therefore, this iteration does NOT use:

- Fabric Lakehouse
- Fabric Warehouse
- Fabric Data Factory
- Fabric notebooks
- Fabric pipelines

Power BI Desktop + PBIP + local data are the primary execution environment.

---

## 1.3 Power BI is the execution environment

The system should work against a Power BI Project (`.pbip`).

Power BI Desktop remains the final authority for whether the generated artifact is usable.

The AI must not simply generate arbitrary PBIP/PBIR files and assume they work.

---

## 1.4 Groq is the reasoning layer

Groq should be used as much as practical to reduce cost and latency.

Groq is responsible for:

- understanding requirements
- interpreting data metadata
- identifying facts and dimensions
- proposing relationships
- selecting KPIs
- planning report pages
- selecting suitable visuals
- diagnosing validation failures
- deciding corrective actions
- explaining results

Power BI Skills are responsible for execution.

---

## 1.5 Power BI Skills are the hands

Existing Power BI Skills/MCP capabilities in VS Code should be reused.

Do not recreate capabilities that already exist.

The system should discover and use available capabilities for:

- project inspection
- semantic model inspection
- DAX/model operations
- report/page/visual operations
- semantic model queries
- validation

The exact available skill operations must be discovered before implementation.

---

# 2. Current Repository

Current structure:

```text
pbi/
├── data/
│   └── power_bi_jira_defect_test_data.xlsx
│
├── docs/
│
├── powerbi/
│   ├── JiraDefectIntelligence.Report/
│   ├── JiraDefectIntelligence.SemanticModel/
│   ├── JiraDefectIntelligence.pbip
│   └── JiraDefectIntelligence.pbix
│
├── prompts/
├── tests/
├── venv/
│
├── .env
├── main.py
├── requirements.txt
└── power_bi_groq_incremental_plan.md
```

The existing Power BI project opens successfully.

The Excel data has already been prepared with queries such as:

```text
FactDefects
DimProject
DimDate
DimPriority
DimStatus
ExpectedKPIs
MonthlyTrend
```

The current project may contain intentional/incomplete model relationships.

**Do not manually fix these as the next step.**

They should become the first test case for AI-driven inspection and correction.

---

# 3. What We Are Building

The final target is a reusable pipeline:

```text
                 DATA
                   |
                   v
          ┌────────────────┐
          │ Data Inspector │
          └───────┬────────┘
                  |
                  v
          ┌────────────────┐
          │  Model Planner │
          └───────┬────────┘
                  |
                  v
          ┌────────────────┐
          │ Model Builder  │
          │ Power BI Skill │
          └───────┬────────┘
                  |
                  v
          ┌────────────────┐
          │ Model Validator│
          └───────┬────────┘
                  |
                  v
          ┌────────────────┐
          │  KPI Planner   │
          └───────┬────────┘
                  |
                  v
          ┌────────────────┐
          │ Report Planner │
          └───────┬────────┘
                  |
                  v
          ┌────────────────┐
          │ Report Builder │
          │ Power BI Skill │
          └───────┬────────┘
                  |
                  v
          ┌────────────────┐
          │ Report Validator│
          └───────┬────────┘
                  |
            PASS / REPAIR
```

This is a logical architecture, not a requirement to create separate Python classes or agents immediately.

---

# 4. Incremental Development Strategy

Do not attempt the full system in one shot.

Build **vertical slices**.

Each slice must provide something useful and prove one part of the architecture.

```text
Slice 1 → Inspect
Slice 2 → Plan
Slice 3 → Execute one change
Slice 4 → Validate/repair
Slice 5 → Generate measures
Slice 6 → Generate one report page
Slice 7 → Generate complete report
Slice 8 → Generalize to new datasets
```

---

# 5. Phase 0 — Protect the Baseline

## Objective

Establish a known-good Git checkpoint.

Already completed:

```text
baseline: Power BI Jira defect project
```

Before every major experiment:

```bash
git status
```

After successful milestones:

```bash
git add .
git commit -m "milestone: <description>"
```

Never destroy the known-good baseline.

---

# 6. Phase 1 — Discover Existing Power BI Skills

## Objective

Understand exactly what is already available in VS Code.

Do NOT write the AI workflow yet.

Inspect the installed Power BI Skills/MCP tools.

Document:

```text
Skill/tool name
Purpose
Inputs
Outputs
Read-only or modifying
Can operate on PBIP?
Can inspect semantic model?
Can modify model?
Can create measures?
Can create pages?
Can create visuals?
Can query data?
Can validate?
```

Create:

```text
docs/powerbi_skills_inventory.md
```

Example:

```text
inspect_project
inspect_semantic_model
query_model
create_measure
modify_model
create_page
create_visual
validate
```

The actual names must come from the installed tools.

---

# 7. Phase 2 — Build a Read-Only Project Inspector

## Objective

Create the first real AI capability.

Do not modify Power BI yet.

Input:

```text
Existing PBIP
```

Power BI Skill gathers metadata.

Groq receives only the relevant metadata.

The system should determine:

```text
Project structure
Tables
Columns
Measures
Relationships
Data types
Potential fact tables
Potential dimensions
Date columns
Existing report pages
Existing visuals
Potential problems
```

Example output:

```json
{
  "project": "JiraDefectIntelligence",
  "fact_tables": ["FactDefects"],
  "dimensions": [
    "DimProject",
    "DimPriority",
    "DimStatus",
    "DimDate"
  ],
  "date_columns": [
    "FactDefects.CreatedDate"
  ],
  "issues": [
    "DimProject column names appear invalid",
    "Date relationship appears missing"
  ]
}
```

### Exit criterion

The system can inspect the current project and explain what is wrong without changing it.

---

# 8. Phase 3 — AI Model Planner

## Objective

Turn inspection results into an implementation plan.

Groq should generate a structured model plan.

Example:

```json
{
  "fact_tables": [
    "FactDefects"
  ],
  "dimensions": [
    "DimProject",
    "DimPriority",
    "DimStatus",
    "DimDate"
  ],
  "relationships": [
    {
      "from": "DimProject.ProjectCode",
      "to": "FactDefects.ProjectCode",
      "cardinality": "1:*"
    },
    {
      "from": "DimPriority.Priority",
      "to": "FactDefects.Priority",
      "cardinality": "1:*"
    },
    {
      "from": "DimStatus.Status",
      "to": "FactDefects.Status",
      "cardinality": "1:*"
    },
    {
      "from": "DimDate.Date",
      "to": "FactDefects.CreatedDate",
      "cardinality": "1:*"
    }
  ]
}
```

The plan should also identify:

- unnecessary tables
- malformed fields
- duplicate structures
- missing relationships
- ambiguous date logic
- required model corrections

### Important

The planner does not directly modify Power BI.

It creates a structured plan for the executor.

---

# 9. Phase 4 — Execute ONE Controlled Model Change

## Objective

Prove that AI can plan a change and Power BI Skills can execute it.

Do not fix the entire model at once.

Pick exactly one issue.

For example:

```text
Missing:
DimDate.Date
      →
FactDefects.CreatedDate
```

Groq decides:

```text
Required action:
Create a 1:* relationship.
```

Power BI Skill performs it.

Then inspect the result.

---

# 10. Phase 5 — Model Validation

## Objective

Verify that the change actually happened.

Validation should ask Power BI:

```text
Does the relationship exist?
Is cardinality correct?
Are the tables present?
Are there model errors?
Can the semantic model be queried?
```

Expected:

```text
PLAN:
DimDate.Date → FactDefects.CreatedDate

ACTUAL:
DimDate.Date → FactDefects.CreatedDate

RESULT:
PASS
```

Only after this works should the system be allowed to perform the next correction.

---

# 11. Phase 6 — Add Repair Loop

Now introduce the first genuinely agentic loop:

```text
        PLAN
          |
          v
       EXECUTE
          |
          v
       VALIDATE
          |
      +---+---+
      |       |
    PASS     FAIL
      |       |
      v       v
    DONE    GROQ
              |
              v
          REPLAN/REPAIR
              |
              v
           EXECUTE
```

Limit retries.

Example:

```text
MAX_REPAIR_ATTEMPTS = 2
```

Never create an infinite loop.

---

# 12. Phase 7 — Semantic Model Understanding

Once model repair works, expand inspection.

The AI should understand:

### Tables

```text
Fact
Dimension
Lookup
Validation
Derived/Aggregated
```

### Columns

```text
ID
Text
Date
Numeric
Boolean
Categorical
Measure candidate
```

### Relationships

```text
1:*
*:1
1:1
inactive
ambiguous
```

### Business meaning

For Jira data:

```text
Defect
Project
Priority
Status
SLA
Age
Customer Impact
Environment
```

This metadata becomes the context for report planning.

---

# 13. Phase 8 — KPI Planner

## Objective

Let Groq determine useful KPIs based on the actual dataset.

Do not hardcode Jira KPIs into the architecture.

For the current test case, Groq may identify:

```text
Total Defects
Open Defects
Closed Defects
High/Highest Defects
SLA Breached
Reopened Defects
Average Age
```

For another dataset it might identify:

```text
Revenue
Gross Margin
Orders
Conversion Rate
Average Order Value
```

This is the point where the solution becomes reusable.

---

# 14. Phase 9 — KPI Builder

Power BI Skills create the required measures.

The system should prefer:

```text
Existing column
        ↓
Existing measure
        ↓
New DAX measure only if necessary
```

Do not create duplicate measures unnecessarily.

Every generated measure should have:

```text
Name
Expression
Purpose
Dependencies
```

---

# 15. Phase 10 — KPI Validation

The system should query Power BI to validate measures.

For the Jira test case, `ExpectedKPIs` can act as the test oracle.

Example:

```text
Measure             Expected    Actual     Result
--------------------------------------------------
Total Defects          1203       1203      PASS
Open Defects            849        849      PASS
Reopened                127        127      PASS
```

The exact expected values must come from the current test data/model rather than assumptions.

If the project uses a different dataset and no expected values exist, validation should instead use:

- semantic consistency
- known totals
- sample calculations
- business rules supplied by the user
- query cross-checks

---

# 16. Phase 11 — Report Requirement Generator

The user should be able to provide a lightweight requirement such as:

```text
Create a stakeholder dashboard for Jira defect health.
Focus on backlog, severity, SLA, aging and project risk.
```

Groq turns that into a report plan.

Example:

```json
{
  "pages": [
    {
      "name": "Executive Overview",
      "purpose": "Overall defect health"
    },
    {
      "name": "Defect Health",
      "purpose": "Priority and status analysis"
    },
    {
      "name": "SLA and Aging",
      "purpose": "Identify overdue and aging defects"
    },
    {
      "name": "Project Analysis",
      "purpose": "Compare project-level risk"
    },
    {
      "name": "Trend Analysis",
      "purpose": "Analyze defects over time"
    }
  ]
}
```

The number of pages should be determined by the requirement and data complexity.

Do not always generate five pages.

---

# 17. Phase 12 — Generate ONE Report Page

Before attempting a complete report, prove one page.

Example:

## Executive Overview

Possible visuals:

```text
KPI Cards
- Total Defects
- Open Defects
- SLA Breached
- High/Highest
- Reopened

Bar chart
- Defects by Project

Column chart
- Defects by Priority

Slicer
- Project
```

Groq determines the visual intent.

Power BI Skill performs the implementation.

---

# 18. Phase 13 — Validate ONE Report Page

Validation must confirm:

```text
Page exists
Visual exists
Visual references valid fields
Visual references valid measures
Filters are valid
No broken references
Measures return data
```

If possible, query the semantic model behind the visual to confirm that the visual is meaningful.

---

# 19. Phase 14 — Full Report Generation

Only after the one-page vertical slice works:

```text
Requirements
   ↓
Model understanding
   ↓
KPI planning
   ↓
KPI creation
   ↓
KPI validation
   ↓
Page planning
   ↓
Page creation
   ↓
Visual creation
   ↓
Page validation
   ↓
Report validation
```

The system can then generate multiple stakeholder-oriented pages.

---

# 20. Phase 15 — Final Artifact Validation

Before declaring success:

```text
PBIP exists
    ↓
Semantic model validates
    ↓
Measures validate
    ↓
Report pages validate
    ↓
Visual references validate
    ↓
Power BI Desktop opens project
    ↓
Project can be saved
    ↓
Project can be reopened
```

Only then:

```text
STATUS = SUCCESS
```

---

# 21. Generalization Test

This is the most important test of whether the architecture is actually reusable.

After the Jira project works, provide a different dataset.

Example:

```text
customer_support_tickets.xlsx
```

Do NOT manually create:

- dimensions
- relationships
- measures
- report pages

Run the same pipeline.

Expected:

```text
New dataset
    ↓
AI inspection
    ↓
AI model plan
    ↓
Power BI implementation
    ↓
AI KPI plan
    ↓
Power BI measures
    ↓
AI report plan
    ↓
Power BI report
    ↓
Validation
```

If manual intervention is still required for normal cases, identify why and improve the skills/workflow.

This is the real proof of reusability.

---

# 22. Token-Efficiency Strategy

Groq should not receive the entire dataset unless absolutely necessary.

## Bad

```text
120,000 rows
      ↓
Groq
```

## Good

```text
Dataset
  ↓
Power Query / Python profiling
  ↓
Metadata
  ↓
Column statistics
  ↓
Small representative samples
  ↓
Groq
```

Example metadata:

```text
Table: FactDefects
Rows: 1203

Columns:
ProjectCode: text, 5 unique values
Priority: categorical, 4 values
Status: categorical, 5 values
CreatedDate: date
AgeDays: numeric
SLABreached: categorical, 2 values
```

Only send actual rows when needed.

---

# 23. Model Routing Strategy

Use Groq economically.

### Smaller/cheaper model

Use for:

- classification
- extraction
- metadata interpretation
- formatting
- simple planning
- straightforward validation explanations

### Larger GPT-OSS model

Use for:

- complex semantic-model reasoning
- report planning
- ambiguous business requirements
- repair decisions
- multi-step analysis

Do not automatically use the largest model for every call.

---

# 24. Structured Outputs

AI should communicate with the orchestrator using structured JSON wherever possible.

Example:

```json
{
  "status": "needs_change",
  "reason": "Date relationship missing",
  "actions": [
    {
      "operation": "create_relationship",
      "from": "DimDate.Date",
      "to": "FactDefects.CreatedDate",
      "cardinality": "1:*"
    }
  ]
}
```

This is much safer than parsing free-form prose.

---

# 25. Prompt Architecture

Keep prompts small and role-specific.

Suggested files:

```text
prompts/
├── inspect.md
├── model_plan.md
├── model_repair.md
├── kpi_plan.md
├── report_plan.md
├── visual_plan.md
└── validate.md
```

Do not put the entire project context into every prompt.

Each prompt should receive only the context it needs.

---

# 26. Python Orchestrator

Initially keep `main.py` simple.

Conceptually:

```text
main.py

1. Load configuration
2. Discover Power BI project
3. Inspect project
4. Ask Groq for model assessment
5. Ask Groq for model plan
6. Execute approved Power BI actions
7. Validate
8. Repair if needed
9. Plan KPIs
10. Build KPIs
11. Validate KPIs
12. Plan report
13. Build report
14. Validate report
15. Produce final summary
```

Do not create a framework around this until complexity requires it.

---

# 27. Human Approval Strategy

For early development, use approval gates.

Example:

```text
AI proposes:
Create relationship X

        ↓

USER APPROVAL

        ↓

Power BI Skill executes
```

Later, once confidence is established, low-risk operations can become automatic.

For example:

### Auto-approved

- read-only inspection
- querying
- validation
- adding a clearly missing measure

### Approval required

- deleting tables
- deleting measures
- changing major model structure
- deleting report pages
- replacing existing visuals
- destructive transformations

This prevents the AI from damaging the project.

---

# 28. Git Strategy

Use Git as the recovery mechanism.

Recommended milestone commits:

```text
baseline: Power BI Jira defect project

milestone: Power BI skills inventory

milestone: AI project inspector

milestone: AI model planner

milestone: first automated model change

milestone: model validation and repair loop

milestone: KPI generation

milestone: KPI validation

milestone: first generated report page

milestone: report validation

milestone: complete Jira report

milestone: reusable dataset test
```

Never experiment without a recoverable state.

---

# 29. Failure Handling

Every operation should produce:

```text
ACTION
RESULT
VALIDATION
```

Example:

```text
ACTION:
Create relationship DimDate.Date → FactDefects.CreatedDate

RESULT:
Power BI Skill reported success

VALIDATION:
Relationship not found

STATUS:
FAIL

NEXT:
Groq diagnose and propose repair
```

The system should never treat:

> "Tool said success"

as equivalent to:

> "Power BI project is correct."

---

# 30. Observability

Keep a lightweight execution log.

Example:

```text
logs/
└── latest_run.json
```

Store:

```text
timestamp
operation
model used
input summary
tool called
tool result
validation result
repair attempts
final status
```

Do not store unnecessary raw business data.

This will be extremely useful when debugging the automation.

---

# 31. What NOT to Build Yet

Do not introduce these until the basic reusable pipeline works:

```text
LangGraph
Multi-agent framework
Agent memory
RAG
Vector database
Fabric
Lakehouse
Warehouse
Jira API integration
Production deployment
Cloud orchestration
Complex UI
Autonomous scheduling
```

The simple Python orchestration is enough.

---

# 32. First Real Vertical Slice

This is the immediate target.

## Input

Existing:

```text
JiraDefectIntelligence.pbip
```

## Step 1

Power BI Skill:

```text
Inspect project
```

## Step 2

Groq:

```text
Understand current model
```

## Step 3

Groq:

```text
Produce model correction plan
```

## Step 4

Power BI Skill:

```text
Execute ONE correction
```

## Step 5

Power BI Skill:

```text
Validate correction
```

## Step 6

If failed:

```text
Groq diagnoses
        ↓
Power BI Skill repairs
        ↓
Validate
```

## Step 7

Power BI Desktop:

```text
Open/reload project
```

### Success

```text
AI identified a real issue
        ↓
AI planned the correction
        ↓
Power BI Skill performed it
        ↓
System validated it
        ↓
Power BI Desktop accepts project
```

That is our first **real AI + Power BI automation milestone**.

---

# 33. Second Vertical Slice

After Slice 1:

```text
Inspect model
     ↓
AI chooses KPIs
     ↓
Power BI creates measures
     ↓
Validate measures
```

Success means the AI can determine useful metrics from the dataset without us manually specifying every DAX measure.

---

# 34. Third Vertical Slice

Then:

```text
Model
 ↓
AI report plan
 ↓
Power BI creates ONE page
 ↓
Validate page
 ↓
Power BI Desktop opens
```

This proves report generation.

---

# 35. Fourth Vertical Slice

Then:

```text
Data
 ↓
Model
 ↓
KPIs
 ↓
Report plan
 ↓
Multiple pages
 ↓
Visuals
 ↓
Validation
 ↓
Working PBIP
```

This is the first complete automated report.

---

# 36. Fifth Vertical Slice — New Dataset

Replace Jira data with another realistic dataset.

The same code should run.

The only user inputs should be approximately:

```text
DATA:
path/to/data.xlsx

REQUIREMENT:
Create a stakeholder report for <business purpose>.
```

Everything else should be discovered/generated by the system.

---

# 37. Definition of Done

The reusable MVP is successful when:

### Data

- [ ] User provides a dataset.
- [ ] System profiles it automatically.
- [ ] System does not require manual schema mapping for normal cases.

### Semantic Model

- [ ] AI identifies fact/dimension structures.
- [ ] AI proposes relationships.
- [ ] Power BI Skills execute model changes.
- [ ] Model is automatically validated.
- [ ] Repair loop can correct simple failures.

### KPIs

- [ ] AI identifies useful KPIs.
- [ ] Power BI Skills create measures.
- [ ] Measures are validated.

### Reports

- [ ] AI determines useful stakeholder pages.
- [ ] AI determines visual intent.
- [ ] Power BI Skills create pages/visuals.
- [ ] Visuals are validated.

### Reliability

- [ ] PBIP opens in Power BI Desktop.
- [ ] PBIP can be reopened after generation.
- [ ] Validation catches failures.
- [ ] Git provides rollback.

### Reusability

- [ ] Same workflow can process a different dataset.
- [ ] Manual model/report construction is not required for normal cases.

---

# 38. Final Target Architecture

Eventually:

```text
                         USER
                           |
                  Data + Business Goal
                           |
                           v
                  ┌─────────────────┐
                  │ Python Workflow │
                  │   Orchestrator  │
                  └────────┬────────┘
                           |
                           v
                    ┌─────────────┐
                    │    GROQ     │
                    │  Reasoning  │
                    └──────┬──────┘
                           |
             Plan / Diagnose / Interpret
                           |
                           v
                ┌─────────────────────┐
                │   Power BI Skills   │
                │                     │
                │ Inspect             │
                │ Query               │
                │ Modify Model        │
                │ Create Measures     │
                │ Create Report       │
                │ Validate            │
                └──────────┬──────────┘
                           |
                           v
                  ┌─────────────────┐
                  │   Power BI PBIP │
                  └────────┬────────┘
                           |
                           v
                    ┌─────────────┐
                    │  Validator  │
                    └──────┬──────┘
                           |
                     PASS / FAIL
                           |
                    FAIL ──┘
                     |
                     v
                   GROQ
                     |
                     v
                  REPAIR
```

---

# 39. The Core Philosophy

The project is **not**:

> "Use AI to write some Power BI files."

The project is:

> **"Build a closed-loop AI system that can understand a dataset, reason about a Power BI solution, operate Power BI through its available skills, observe the result, validate it, and repair problems."**

The distinction matters.

The AI should not blindly generate artifacts.

It should:

```text
UNDERSTAND
    ↓
PLAN
    ↓
ACT
    ↓
OBSERVE
    ↓
VALIDATE
    ↓
REPAIR
    ↓
DELIVER
```

And we should build exactly that loop **incrementally**, starting with one real correction on the existing Jira project.

---

# 40. Immediate Next Action

Do NOT manually fix the current `DimProject`, `DimDate`, or `MonthlyTrend` issues.

The next development task is:

> **Inventory the Power BI Skills already installed in VS Code.**

Once the available tools and their exact operations are known, implement:

```text
main.py
   ↓
Power BI project inspection
   ↓
Groq assessment
   ↓
structured correction plan
```

No report generation yet.

No LangGraph.

No new framework.

No unnecessary abstraction.

The first milestone is to prove that **AI can look at the existing Power BI project and understand what needs to be done.**

That becomes the foundation for everything else.