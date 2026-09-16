# STAGE 2 — REPORT SHELL, THEME AND NAVIGATION

Implement ONLY the report shell approved by Stage 0.

IMPORTANT:
- Load and use:
  - powerbi-report-design
  - powerbi-report-authoring
- Use the Stage 0 report/page/navigation/theme contract.
- Do NOT create analytical visuals yet.
- Do NOT modify the semantic model.
- Keep existing valid slicers unless the plan explicitly changes them.
- Work page-by-page and validate after implementation.
- Keep token usage low.

## THEME

Check:

`theme/theme.json`

### If a user theme exists:
- use it as the report theme
- register/apply it to the report
- preserve its intended colors, fonts and styling
- do not replace it with an invented theme

### If no theme exists:
- create a professional executive theme based on the Stage 0 theme plan
- save it under:

`theme/theme.json`

The theme must be reusable for future datasets/projects.

## PAGE STRUCTURE

Create/repair the approved pages only.

For every page establish:

- page name
- page order
- canvas size
- background
- header
- page title
- subtitle if approved
- filter/slicer region
- analytical content region
- navigation region

Target:

`1920 × 1080`

Use a consistent layout grid.

## NAVIGATION

Use the Stage 0 navigation plan.

Preferred layout:

TOP NAVIGATION BAR

Place navigation:
- horizontally
- consistently
- below the page title/header
- aligned to the report content area

OR, if Stage 0 explicitly selected it:

LEFT NAVIGATION BAR

Do NOT leave navigation floating in an arbitrary location.

Navigation must:
- have consistent size
- have consistent spacing
- clearly indicate the active page
- point to valid target pages
- remain usable at normal report zoom

## VISUAL DENSITY

Do not create a sparse college-project layout.

Reserve enough content space for approximately:

- 5–8 analytical visuals per analytical page

The actual number must depend on the approved Stage 0 visual plan.

Use:
- balanced cards
- charts
- tables/matrices
- appropriate whitespace

Avoid:
- oversized empty regions
- giant decorative headers
- unnecessary whitespace
- excessive cards

## IMPLEMENTATION

Implement:

1. Theme
2. Page structure
3. Header/title
4. Navigation
5. Slicer/filter areas
6. Consistent page backgrounds
7. Consistent alignment/grid

Do not create analytical visuals.

## VALIDATION

After implementation validate:

- PBIR structure
- page count
- page order
- page dimensions
- theme registration
- background
- title
- slicers
- navigation
- navigation targets
- positions
- canvas bounds
- cross-page consistency

If Power BI Desktop CLI is available:

- open/reload
- refresh
- verify report opens without errors
- render/screenshot each page
- inspect screenshots for:
  - misplaced navigation
  - clipping
  - overlapping objects
  - unreadable text
  - incorrect theme
  - excessive empty space

## FAILURE / CORRECTION

If anything fails:

PLAN → IDENTIFY FAILURE → MINIMAL FIX → VALIDATE AGAIN

Never rebuild the entire report.

## ACCEPTANCE CRITERIA

PASS requires:

- theme applied
- theme sourced from `theme/theme.json`
- pages correct
- navigation correctly positioned
- navigation works
- consistent shell
- medium-density layout reserved
- no semantic-model changes
- PBIR validation passes
- Desktop reload/refresh passes when available
- rendered pages visually acceptable

## OUTPUT

STATUS: PASS / FAIL

IMPLEMENTED:
- shell changes

THEME:
- theme source and status

NAVIGATION:
- location and validation

PAGE INVENTORY:
- pages created/modified

VALIDATION:
- static
- Desktop
- screenshot/render

CORRECTIONS:
- any fixes performed

ERRORS:
- none or exact errors

READY FOR STAGE 3:
- YES / NO