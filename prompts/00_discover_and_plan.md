# STAGE 0 — DISCOVER, ANALYZE AND PLAN

You are working on a Power BI project with data already loaded.

Your job is to analyze the existing Power BI project and create an implementation-ready report plan.

IMPORTANT:
- Do NOT modify any Power BI files in this stage.
- Do NOT create visuals.
- Do NOT repair the semantic model.
- Do NOT guess missing business meanings.
- Do NOT start implementation.
- Use the available Power BI skills, especially:
  - powerbi-report-design
  - semantic-model-authoring
  - powerbi-report-authoring
- Prefer the Power BI project files and model metadata over assumptions.
- Be token-efficient. Do not repeatedly inspect the same files.

## STEP 1 — INVENTORY

Inspect:
- PBIP structure
- Semantic model
- Tables
- Columns
- Data types
- Existing relationships
- Existing measures
- Existing report pages
- Existing visuals
- Existing slicers
- Existing navigation
- Existing theme
- Report/page dimensions
- Existing formatting

Also inspect the project `theme/` folder.

If a user-provided theme exists:
- treat it as the required report theme
- do not replace it
- do not invent another theme

If no theme exists:
- plan a professional executive theme
- clearly state that a default theme will be created during Stage 2.

## STEP 2 — ANALYZE THE DATA

Determine:
- fact tables and their grain
- dimensions
- candidate keys
- important categorical fields
- important dates
- important measures
- business metrics supported by the data
- useful dimensions for slicing
- potential executive KPIs
- potential operational/detail analysis

Do not create business logic that cannot be supported by the data.

## STEP 3 — DESIGN THE REPORT

Create an executive-level report, NOT a college-project dashboard.

Target:
- medium visual density
- clear hierarchy
- meaningful whitespace
- professional typography
- consistent alignment
- limited visual clutter
- approximately 5–8 analytical visuals per analytical page where the data supports it
- do not artificially add visuals merely to increase the count

Recommended page structure should normally include:

1. Executive / Overview
2. Risk / Performance / Operational Analysis
3. Trend / Mix / Drivers
4. Detail / Drill-down

Adapt this to the dataset when appropriate.

## NAVIGATION

Use ONE consistent navigation pattern across all pages:

Preferred:
- horizontal navigation bar at the TOP, below the page title/header

Alternative:
- vertical navigation bar on the LEFT

Do NOT place navigation in an awkward floating position.

Use the same position, size, spacing and style on every page.

## VISUAL DESIGN

For every planned visual define:
- page
- visual name
- visual type
- purpose
- fields
- measures
- filters if required
- sorting
- position
- size
- formatting intent

Use modern Power BI visual types supported by the available authoring skill.

Prefer:
- KPI cards
- bar/column charts
- line charts
- stacked charts where useful
- tables/matrices for operational detail
- appropriate slicers

Avoid unnecessary:
- pie/donut charts
- gauges
- decorative visuals
- redundant KPIs
- duplicate charts

## THEME

Define:
- background
- surface/card color
- primary text
- secondary text
- accent colors
- positive/negative colors if required
- font family
- visual title style
- slicer style
- navigation style

If `theme/theme.json` exists, use it as the source of truth.

## ACCEPTANCE CRITERIA

The Stage 0 plan is PASS only if it contains:

1. Data/model assessment
2. Proposed semantic model changes
3. Page list and purpose
4. Navigation design
5. Theme strategy
6. Visual plan for every page
7. Approximate visual count per page
8. Field/measure bindings
9. Layout coordinates or layout regions
10. Validation strategy
11. HITL checkpoints
12. Explicit technical acceptance criteria

Create a machine-readable implementation contract:

`visual_plan.json`

and, where useful:

`semantic_model_plan.json`

Do not implement anything.

## OUTPUT

Return:

STATUS: PASS or FAIL

PLAN:
- concise summary of the proposed report

MODEL PLAN:
- required semantic model changes

PAGE PLAN:
- pages and purpose

NAVIGATION PLAN:
- exact navigation approach

THEME PLAN:
- source and usage of theme

VISUAL PLAN:
- visual count and visual contracts per page

VALIDATION PLAN:
- static validation
- PBIR validation
- Power BI Desktop refresh
- screenshot/render validation
- final QA

ACCEPTANCE CRITERIA:
- exact conditions required for Stage 0 completion

If required information cannot be established from the project, mark the relevant item as UNKNOWN rather than guessing.