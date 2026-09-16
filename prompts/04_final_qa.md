# STAGE 4 — FINAL END-TO-END QA

Perform final QA of the complete Power BI report.

IMPORTANT:
- This is validation, not redesign.
- Do not make speculative changes.
- Do not add visuals.
- Do not change the semantic model unless a critical technical defect is found.
- Use the Stage 0 contracts as the source of truth.
- Use all available Power BI skills/tools.
- Power BI Desktop CLI MUST be used when available.

## STEP 1 — STATIC VALIDATION

Validate:

- PBIP structure
- PBIR structure
- TMDL structure
- report definition
- page definitions
- visual definitions

Required:

`Errors = 0`

`Warnings = 0`

## STEP 2 — SEMANTIC MODEL QA

Check:

- tables
- columns
- data types
- keys
- relationships
- date model
- measures
- DAX references
- invalid references

Compare against:

`semantic_model_plan.json`

## STEP 3 — REPORT QA

Check:

- page count
- page order
- page names
- canvas dimensions
- theme
- page backgrounds
- titles
- navigation
- navigation targets
- slicers
- visual count

Compare against:

`visual_plan.json`

## STEP 4 — VISUAL CONTRACT QA

For every approved visual check:

- visual type
- title
- fields
- measures
- filters
- sorting
- position
- size
- canvas bounds
- formatting

No unapproved analytical visuals may exist.

## STEP 5 — POWER BI DESKTOP QA

If Power BI Desktop CLI is available:

1. Open the PBIP/report.
2. Reload the report.
3. Refresh the semantic model.
4. Capture refresh result.
5. Check for model/query errors.
6. Render every report page.
7. Capture screenshots/previews.

Validate screenshots for:

- page title
- navigation placement
- theme
- alignment
- clipping
- overlapping visuals
- empty regions
- visual readability
- slicer readability
- consistent spacing
- overall executive quality

## STEP 6 — EXECUTIVE QUALITY REVIEW

The report must not look like a college project.

Check:

- medium visual density
- clear visual hierarchy
- consistent navigation
- consistent theme
- meaningful KPIs
- useful analytical coverage
- no redundant visuals
- no oversized empty areas
- no unnecessary decorative elements
- consistent typography
- consistent spacing

## STEP 7 — SCOPE CHECK

Confirm:

- no unintended semantic-model changes
- no unintended report changes
- no unrelated files changed
- no theme changes outside the approved theme
- no navigation regressions

Run:

`git diff --check`

and inspect changed files.

## FAILURE / CORRECTION PROTOCOL

If any QA test fails:

STATUS: FAIL

Identify:

- failed test
- affected file/object
- root cause
- smallest corrective action

Then:

FIX → VALIDATE → RE-RUN FAILED TESTS

Do NOT restart the entire workflow.

If the failure cannot be safely corrected automatically, stop and report the exact blocker.

## FINAL ACCEPTANCE CRITERIA

A report is READY FOR DELIVERY only when ALL are PASS:

A. PBIP/PBIR validation
B. Semantic model
C. Relationships
D. Date model
E. Measures/DAX
F. Theme
G. Page structure
H. Navigation
I. Visual inventory
J. Visual contracts
K. Desktop reload
L. Desktop refresh
M. Page rendering
N. Screenshot/layout QA
O. HITL approval
P. Cross-page scope
Q. Git/diff check
R. No unexpected changes

## OUTPUT

# FINAL QA

STATUS: PASS / FAIL

TECHNICAL:
- PBIP/PBIR
- Semantic model
- DAX
- relationships
- date model

REPORT:
- pages
- theme
- navigation
- visuals
- visual contracts

POWER BI DESKTOP:
- reload
- refresh
- rendering
- screenshots

DESIGN:
- density
- alignment
- readability
- executive quality

SCOPE:
- unexpected changes

CORRECTIONS:
- fixes performed

ERRORS:
- none or exact blockers

FINAL DECISION:

READY FOR DELIVERY
or
NOT READY FOR DELIVERY