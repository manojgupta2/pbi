# Simple End-to-End Power BI + Groq MVP
## Incremental plan — no LangGraph, no Fabric, no over-engineering

> **Goal of this iteration:** prove one small, reliable end-to-end flow using the data we already have, Power BI, the Power BI skills already installed in VS Code, and Groq.
>
> **We are NOT building a multi-agent system in this iteration.**
>
> **We are NOT using LangGraph.**
>
> **We are NOT generating a Power BI report from scratch with AI.**
>
> **We are NOT using Fabric Lakehouse/Warehouse.**
>
> The first objective is reliability: **the Power BI project must open in Power BI Desktop before and after anything our automation touches.**

---

# 1. What We Are Actually Building

Our first version should be deliberately boring.

```text
                 Test Excel Data
                       |
                       v
              Power BI Desktop
                       |
                       v
              Known-good PBIP
                       |
                       |
              Power BI Skills
                in VS Code
                       |
                       v
                 Power BI
              Semantic Model
                       |
                       v
                    Groq
                       |
                       v
              Business Insight
```

The first AI workflow is:

```text
User asks a question
        |
        v
Simple Python application
        |
        v
Groq understands the question
        |
        v
Power BI skill/tool is used
        |
        v
Semantic model is queried
        |
        v
Small structured result
        |
        v
Groq interprets the result
        |
        v
Answer to user
```

That is enough for the first iteration.

---

# 2. The Most Important Design Decision

## Do NOT ask AI to create a Power BI report from scratch.

This is the mistake we are explicitly avoiding.

Power BI projects contain several interdependent artifacts:

```text
PBIP
 |
 +-- Report
 |     |
 |     +-- PBIR definitions
 |
 +-- Semantic Model
       |
       +-- model metadata
       +-- tables
       +-- measures
       +-- relationships
```

A syntactically plausible file is not necessarily a valid Power BI project.

Therefore:

> **Power BI Desktop creates the initial known-good project. AI operates on a project that Power BI has already created and successfully opened.**

This gives us a safe baseline.

---

# 3. Current Project

Current VS Code structure:

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

This is sufficient.

Do not restructure the repository yet.

---

# 4. Scope of This Iteration

## In scope

- Existing Excel test data
- Power BI Desktop
- Power BI Project (`.pbip`)
- Existing Power BI skills in VS Code
- Existing Power BI MCP/tooling where available
- Groq
- One simple Python orchestration script
- Semantic-model querying
- KPI analysis
- One controlled Power BI modification later
- Validation that the PBIP still opens

## Explicitly out of scope

- LangGraph
- Fabric Lakehouse
- Fabric Warehouse
- Data pipelines
- Multiple agents
- Agent memory
- Complex orchestration
- Autonomous report redesign
- Full report generation from scratch
- Jira API integration
- Production deployment
- Scheduled refresh
- RAG/vector databases
- Large-scale prompt frameworks

---

# 5. Target MVP

At the end of this iteration, we want to demonstrate this:

### User

> Which project has the highest defect risk?

### System

```text
1. Groq understands the request
        |
2. Power BI skill/tool inspects model if needed
        |
3. Power BI returns aggregated project-level data
        |
4. Groq analyzes the result
        |
5. System returns evidence-based answer
```

For example:

```text
Highest risk project: OMEN-DE

Evidence:
- Highest open-defect backlog
- High SLA-breach count
- Significant high/critical backlog

Recommendation:
Prioritize SLA-breached High/Highest defects for triage.
```

The important part is that the numbers come from **Power BI**, not from Groq's imagination.

---

# 6. Phase 0 — Stop and Establish a Known-Good Power BI Project

## Objective

Get a Power BI project that opens successfully.

Do this before writing AI automation.

### Step 0.1

Open:

```text
powerbi/JiraDefectIntelligence.pbip
```

in Power BI Desktop.

### Step 0.2

If it opens successfully:

**Do not change anything yet.**

### Step 0.3

Check:

- Report view opens
- Model view opens
- Data is available
- Tables are present
- No obvious model errors

### Step 0.4

Save the project.

### Step 0.5

Close Power BI Desktop.

### Step 0.6

Reopen the same `.pbip`.

This confirms the project is genuinely usable.

---

# 7. Phase 1 — Build Only the Minimum Semantic Model

We need a simple model.

Expected conceptual structure:

```text
                 DimDate
                    |
                    |
DimProject ---- FactDefects ---- DimPriority
                    |
                    |
                DimStatus
```

The exact physical structure should be based on the actual imported data.

Do not add unnecessary tables.

Do not optimize prematurely.

---

# 8. Phase 2 — Create a Tiny KPI Set

We only need enough measures to prove the workflow.

Start with:

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
High + Highest Defects =
CALCULATE(
    [Total Defects],
    FactDefects[Priority] IN {"High", "Highest"}
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

That's enough for MVP.

We do NOT need 50 measures.

---

# 9. Phase 3 — Validate the Data

The test workbook contains expected KPI values.

Initial validation:

| KPI | Expected |
|---|---:|
| Total Defects | 1203 |
| Open Defects | 849 |
| Closed/Resolved | 354 |
| Highest | 137 |
| High | 346 |
| Open High/Highest | 357 |
| Open SLA Breached | 813 |
| All SLA Breached | 1097 |
| Reopened | 127 |

The exact values should be verified against the current workbook/model if the data/model has been changed.

## Rule

If the baseline does not match:

> **Stop. Fix Power BI first.**

Do not blame Groq.

---

# 10. Phase 4 — Create a Very Simple Report Manually

This report exists only to provide a known-good stakeholder surface.

Do NOT ask AI to create it.

Create one page:

## `Executive Overview`

Use:

### Cards

- Total Defects
- Open Defects
- High + Highest
- SLA Breached
- Reopened

### One chart

```text
Defects by Project
```

### One chart

```text
Defects by Priority
```

### One slicer

```text
Project
```

That's it.

No fancy dashboard.

No 15 visuals.

No AI-generated layout.

The purpose is to prove:

```text
Data -> Model -> Report -> Power BI Desktop
```

works.

---

# 11. Phase 5 — Create the Golden Baseline

This is the most important checkpoint.

Once the report opens correctly:

```text
Power BI Desktop
      |
      v
Save
      |
      v
Close
      |
      v
Reopen
      |
      v
PASS
```

Then:

```bash
git status
```

Commit:

```bash
git add .
git commit -m "baseline: known-good Power BI project"
```

From this point forward, this is the **golden baseline**.

---

# 12. Phase 6 — Verify Power BI Skills in VS Code

Now we bring AI tooling into the picture.

We already have Power BI skills installed.

Do not build replacements.

First identify exactly what the existing skills can do.

We want to establish:

```text
Skill/tool
    |
    +-- inspect semantic model
    |
    +-- query model
    |
    +-- inspect report
    |
    +-- modify semantic model
    |
    +-- modify report
    |
    +-- validate
```

We do not need all of these immediately.

For MVP, the only required capability is:

> **Read/query the existing semantic model.**

If the skills already expose this, use them directly.

---

# 13. Phase 7 — First Power BI Tool Test Without Groq

Before connecting Groq, test the Power BI capability directly.

Ask the tooling:

> What tables, columns and measures are available in the JiraDefectIntelligence semantic model?

Then:

> What is the total number of defects?

Then:

> Return defects by project.

Expected conceptual output:

```text
Project       Defects
---------------------
OMEN-DE       ...
OMEN-NA       ...
OMEN-AP       ...
...
```

This step isolates Power BI tooling from LLM problems.

## Exit criterion

Power BI tooling can successfully inspect/query the known-good project.

---

# 14. Phase 8 — Connect Groq

Now configure Groq.

Use `.env` for the API key.

Example:

```text
GROQ_API_KEY=...
```

Do not commit `.env`.

The first Python program should be extremely small.

Conceptually:

```text
main.py

    |
    +-- get user question
    |
    +-- call Groq
    |
    +-- obtain structured intent
    |
    +-- call Power BI capability
    |
    +-- send result to Groq
    |
    +-- print answer
```

Do not introduce classes, frameworks or agent abstractions yet.

---

# 15. Phase 9 — First End-to-End AI Flow

The first supported question should be fixed.

For example:

> How many open defects do we have?

Flow:

```text
User
 |
 v
main.py
 |
 v
Groq
 |
 | "Need Open Defects"
 v
Power BI
 |
 | 849
 v
Groq
 |
 v
"Currently there are 849 open defects."
```

This is our first real end-to-end test.

---

# 16. Phase 10 — Expand to Five Questions

Once the first question works, support:

### Q1

> How many total defects are there?

### Q2

> How many open defects are there?

### Q3

> How many High and Highest priority defects are there?

### Q4

> How many SLA-breached defects are there?

### Q5

> How many defects have been reopened?

The model should retrieve the values from Power BI.

---

# 17. Phase 11 — Add One Analytical Question

Now introduce actual reasoning.

Question:

> Which project has the highest defect risk?

Power BI should provide aggregated evidence such as:

```text
Project | Open | High/Highest | SLA Breached | Reopened
```

Groq then reasons over that small dataset.

Important:

```text
Power BI = calculation
Groq     = interpretation
```

Never reverse those responsibilities.

---

# 18. Phase 12 — Make the AI Output Structured

For analytical questions, ask Groq to return:

```json
{
  "answer": "...",
  "risk_level": "HIGH",
  "evidence": [
    "...",
    "...",
    "..."
  ],
  "recommendation": "..."
}
```

This makes the workflow easier to extend later.

---

# 19. Phase 13 — Add a Small Test Suite

Create:

```text
tests/
└── analyst_tests.json
```

Example:

```json
[
  {
    "question": "How many total defects are there?",
    "expected": 1203
  },
  {
    "question": "How many open defects are there?",
    "expected": 849
  },
  {
    "question": "How many reopened defects are there?",
    "expected": 127
  }
]
```

The first tests should validate the deterministic Power BI answer.

Do not test whether Groq "sounds good."

Test the numbers.

---

# 20. Phase 14 — Only Now Test One Controlled Modification

Once this works:

```text
User
 -> Groq
 -> Power BI
 -> Result
 -> Groq
 -> Answer
```

we can test:

```text
User
 -> Groq
 -> Power BI skill
 -> modify existing PBIP
 -> validate
 -> Power BI Desktop
```

But only make **one tiny change**.

Good first candidate:

> Add a measure called `Average Age`.

or:

> Modify the title of an existing visual.

The safest progression is:

```text
read
 ↓
query
 ↓
analyze
 ↓
modify one thing
 ↓
validate
```

---

# 21. Critical Rule for Report Modification

AI must NEVER be allowed to blindly generate an entire `.pbip` or PBIR project.

Instead:

```text
Known-good PBIP
      |
      v
Existing artifact
      |
      v
Skill/tool performs controlled change
      |
      v
Validation
      |
      v
Power BI Desktop opens
```

If the skill/tool cannot guarantee a safe modification, we do the change manually for this iteration.

That is completely acceptable.

The goal of this iteration is **proof of workflow**, not maximum automation.

---

# 22. Phase 15 — Validation Gate

Every future automated modification follows:

```text
              AI change
                  |
                  v
             Validation
                  |
          +-------+-------+
          |               |
        PASS             FAIL
          |               |
          v               v
       Continue        Revert
                          |
                          v
                    Investigate
```

And additionally:

```text
PASS structural validation
        |
        v
Open in Power BI Desktop
        |
        v
PASS
```

This is our strongest protection against spending hours producing a broken Power BI project.

---

# 23. The MVP Architecture

Keep the code approximately this simple:

```text
pbi/
│
├── data/
│
├── powerbi/
│
├── prompts/
│   └── analyst.md
│
├── tests/
│   └── analyst_tests.json
│
├── main.py
├── requirements.txt
└── .env
```

No:

```text
agents/
orchestrator/
state/
graph/
memory/
planner/
reviewer/
router/
```

yet.

---

# 24. Model Strategy

Use Groq primarily for reasoning.

## Default

Use the smaller/cheaper GPT-OSS model for:

- simple question understanding
- intent classification
- formatting
- simple responses

## Stronger model

Use GPT-OSS 120B when the task needs:

- complex reasoning
- risk interpretation
- complicated report requirements
- later-stage planning

Do not route everything to the largest model.

---

# 25. Token-Efficient Design

This is critical.

Bad:

```text
Excel 1203 rows
       |
       v
      Groq
```

Good:

```text
User question
      |
      v
Power BI
      |
      v
5-20 aggregated rows
      |
      v
Groq
```

For example:

```text
Project | Open | SLA Breached | High/Highest
OMEN-DE | 281  | 244          | 156
...
```

Groq does not need the underlying 1,203 rows to determine which project is riskiest.

---

# 26. Prompt Strategy

For MVP, we need only two prompts.

## `prompts/analyst.md`

Core rules:

```text
You are a Power BI analyst.

Power BI is the source of truth for numerical calculations.

Do not invent numbers.

Prefer existing semantic-model measures.

If a question requires data, obtain the data from Power BI.

Use Groq only to interpret the Power BI result.

Keep responses concise and evidence-based.
```

## Optional `prompts/query.md`

Later, when query generation is needed:

```text
Generate the smallest query required to answer the user's question.

Prefer existing measures.

Do not retrieve raw fact rows when an aggregation can answer the question.
```

That's enough initially.

---

# 27. What the First End-to-End Demo Should Look Like

We should be able to demonstrate this in one session.

## Step 1

Open:

```text
JiraDefectIntelligence.pbip
```

Power BI Desktop opens successfully.

## Step 2

Show the report.

## Step 3

Run:

```text
python main.py
```

## Step 4

Ask:

> How many open defects do we have?

## Step 5

System retrieves:

```text
849
```

from Power BI.

## Step 6

Groq generates:

> There are currently 849 open defects.

## Step 7

Ask:

> Which project has the highest SLA risk?

## Step 8

Power BI returns aggregated evidence.

## Step 9

Groq explains the result.

That is a successful MVP.

---

# 28. What We Will Add Later

Once the above works, complexity can be added one layer at a time.

## Iteration 2

Add:

```text
Report inspection
```

AI can understand:

- pages
- visuals
- measures used
- filters

## Iteration 3

Add:

```text
Controlled report modification
```

AI can make one small change.

## Iteration 4

Add:

```text
Validation
+
Regression tests
```

## Iteration 5

Add:

```text
Report planning
```

## Iteration 6

Add:

```text
Plan
 -> Implement
 -> Validate
```

## Iteration 7

Add separate specialized agents if there is a real reason:

```text
Analyst
Planner
Builder
Reviewer
```

## Iteration 8

Add more sophisticated orchestration only if the workflow actually needs it.

**LangGraph is not part of this iteration or the planned architecture for this prototype.**

---

# 29. Future Agent Architecture

Later, when the simple flow is proven, we can evolve toward:

```text
                    User
                      |
                      v
                  Controller
                      |
       +--------------+--------------+
       |              |              |
       v              v              v
    Analyst        Planner         Reviewer
       |              |
       |              v
       |           Builder
       |              |
       +--------------+
              |
              v
          Power BI
```

But that is a **future iteration**.

The MVP remains:

```text
              User
                |
                v
             Groq
                |
                v
        Power BI Skills
                |
                v
       Semantic Model
                |
                v
             Groq
                |
                v
             Answer
```

---

# 30. Definition of Done for This Iteration

We are finished when all of these are true:

### Power BI

- [ ] `.pbip` opens successfully.
- [ ] Semantic model works.
- [ ] Test data is loaded.
- [ ] Core measures work.
- [ ] KPI values are validated.
- [ ] Simple stakeholder page exists.
- [ ] `.pbip` can be closed and reopened.

### VS Code

- [ ] Existing Power BI skills are identified.
- [ ] Power BI skill/tool can inspect the project.
- [ ] Power BI skill/tool can retrieve model information.
- [ ] Power BI skill/tool can execute/query the semantic model.

### Groq

- [ ] Groq connection works.
- [ ] Small model works for simple intent.
- [ ] Stronger model can be used for reasoning when needed.

### End-to-end

- [ ] User can ask a Power BI question.
- [ ] Power BI provides the numbers.
- [ ] Groq interprets the result.
- [ ] Answer is evidence-based.
- [ ] No raw dataset is unnecessarily sent to Groq.

### Safety

- [ ] Golden Git baseline exists.
- [ ] No automated report generation from scratch.
- [ ] Any automated modification is validated.
- [ ] Power BI Desktop remains the final authority that the project is usable.

---

# 31. Exact Work Sequence From Where We Are Today

Do these in this exact order.

```text
1. Open JiraDefectIntelligence.pbip
        |
2. Confirm it opens
        |
3. Inspect Model view
        |
4. Inspect Report view
        |
5. Validate tables
        |
6. Validate core KPIs
        |
7. Create/finish ONE simple report page
        |
8. Close Power BI
        |
9. Reopen PBIP
        |
10. Git commit known-good baseline
        |
11. Test Power BI skill directly
        |
12. Query semantic model without Groq
        |
13. Configure Groq
        |
14. Connect main.py to Groq
        |
15. Implement ONE question
        |
16. Implement FIVE questions
        |
17. Implement ONE analytical question
        |
18. Add structured output
        |
19. Add deterministic tests
        |
20. Test ONE controlled Power BI modification
        |
21. Validate modification
        |
22. Reopen in Power BI Desktop
        |
23. Commit successful change
```

**Stop after each major checkpoint.**

Do not jump from step 1 to step 23.

---

# 32. Success Criterion

The most important success criterion is not:

> "We created a sophisticated AI agent."

It is:

> **"We have a working Power BI project, and Groq can use our existing Power BI capabilities to answer questions from its semantic model reliably."**

Once that works, we have a solid foundation.

Then adding:

```text
planning
+
report authoring
+
validation
+
multiple agents
```

becomes incremental engineering rather than a giant experiment.

---

# 33. Final Principle

## Keep this iteration brutally simple.

```text
                    ┌─────────────┐
                    │    Groq     │
                    │  Reasoning  │
                    └──────┬──────┘
                           │
                           │
                    ┌──────▼──────┐
                    │ Power BI    │
                    │ Skills/MCP  │
                    └──────┬──────┘
                           │
                           │
                    ┌──────▼──────┐
                    │  Semantic   │
                    │    Model    │
                    └─────────────┘
```

**Power BI calculates.**

**Power BI skills provide controlled access.**

**Groq reasons.**

**Python connects the pieces.**

**Power BI Desktop validates the final artifact.**

No LangGraph. No Fabric. No multi-agent architecture. No giant autogenerated PBIR.

First make this small loop work.

Then make it smarter.