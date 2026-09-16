# STAGE 3 — ANALYTICAL VISUAL IMPLEMENTATION

Implement the approved analytical visuals from Stage 0.

IMPORTANT:
- Load:
  - powerbi-report-authoring
  - powerbi-report-design
  - semantic-model-authoring
- Use `visual_plan.json` as the ONLY visual contract.
- Do not invent additional visuals.
- Do not modify the semantic model.
- Do not modify theme/navigation unless explicitly required by the contract.
- Preserve existing slicers and shell.
- Use a HITL sequence.
- Implement ONE visual at a time.
- Validate immediately after every visual.
- Keep token usage low.

## VISUAL DENSITY

The report should have medium visual density.

Target approximately:
- 5–8 meaningful analytical visuals per analytical page

Do NOT blindly add visuals to reach a number.

Every visual must answer a meaningful business question.

## PROCESS

For each visual:

PLAN
→ IMPLEMENT
→ STATIC VALIDATE
→ DESKTOP VALIDATE
→ RENDER/Screenshot
→ HITL REVIEW
→ NEXT VISUAL

Do not implement the next visual until the current visual passes.

## BEFORE EACH VISUAL

Read ONLY its contract from `visual_plan.json`.

Confirm:

- page
- visual name
- purpose
- visual type
- category fields
- values/measures
- series fields
- filters
- sorting
- title
- position
- size
- formatting
- expected interaction

Verify referenced model objects exist.

## IMPLEMENTATION

Use the supported Power BI authoring skill/catalog.

Prefer modern supported visual types.

Do not create unsupported/custom structures when a supported authoring capability exists.

Apply only approved fields and formatting.

## VALIDATION AFTER EACH VISUAL

Run:

1. PBIR validation
2. visual binding validation
3. field/measure reference validation
4. title validation
5. position/size validation
6. canvas-bound validation
7. unexpected-filter validation
8. cross-page scope check

If Power BI Desktop CLI is available:

9. reload/refresh
10. render the affected page
11. inspect the rendered page

Check:
- visual renders
- no errors
- no clipping
- no overlap
- title readable
- labels readable
- correct theme
- correct spacing
- correct interaction with slicers

## HITL

After the visual passes technical validation:

STOP.

Report:

VISUAL READY FOR HITL

Ask the user to review the affected page.

Do not continue automatically unless the user confirms.

Possible responses:

- `done` / `approved` → continue
- change requested → apply only requested change and revalidate
- reject → remove/correct only that visual and revalidate

## FAILURE / CORRECTION

If technical validation fails:

1. Identify exact failure.
2. Compare against visual contract.
3. Make the smallest corrective change.
4. Revalidate.
5. Do not proceed until PASS.

If visual review fails:

1. Capture the requested change.
2. Modify only that visual.
3. Re-render.
4. Revalidate.
5. Ask for HITL again.

## FINAL STAGE 3 VALIDATION

After all visuals are approved:

Validate:

- complete visual inventory
- visual types
- field bindings
- measures
- titles
- sorting
- filters
- positions
- sizes
- canvas bounds
- theme
- navigation
- slicers
- cross-page scope
- semantic-model immutability

Run:

- PBIR validation
- Power BI Desktop reload
- Power BI Desktop refresh
- page rendering/screenshot validation
- git/diff check

## ACCEPTANCE CRITERIA

PASS requires:

- every approved visual implemented
- every visual individually validated
- every visual HITL approved
- medium-density target achieved
- no unnecessary visuals
- no semantic-model changes
- no shell/navigation regression
- Desktop refresh succeeds
- rendered pages have no obvious technical/layout defects

## OUTPUT

For each visual:

STATUS: PASS / FAIL

VISUAL:
- name

CONTRACT:
- PASS / FAIL

TECHNICAL VALIDATION:
- PASS / FAIL

DESKTOP:
- PASS / FAIL

RENDER:
- PASS / FAIL

HITL:
- APPROVED / CHANGE REQUESTED

CORRECTIONS:
- changes made

After all visuals:

STAGE 3 STATUS:
- PASS / FAIL