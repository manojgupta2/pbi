# Power BI AI Report Generation Workflow

This project follows a controlled 5-stage workflow.

Stage 0
-------
Discover → Analyze → Plan

Prompt:
00_discover_and_plan.md

Output:
- visual_plan.json
- semantic_model_plan.json

No implementation.


Stage 1
-------
Semantic Model

Prompt:
01_semantic_model.md

Flow:
Plan → Implement → Validate → Correct if required

Output:
Validated semantic model.


Stage 2
-------
Report Shell

Prompt:
02_report_shell.md

Flow:
Plan → Implement → Validate → Desktop Reload/Refresh → Render

Output:
Validated:
- theme
- pages
- navigation
- headers
- slicers
- layout shell


Stage 3
-------
Visuals

Prompt:
03_visuals.md

Flow:

One visual
    ↓
Implement
    ↓
Validate
    ↓
Desktop refresh
    ↓
Render
    ↓
HITL
    ↓
Approve
    ↓
Next visual

Output:
Fully validated analytical report.


Stage 4
-------
Final QA

Prompt:
04_final_qa.md

Flow:

Static QA
    ↓
Semantic QA
    ↓
Report QA
    ↓
Visual QA
    ↓
Desktop Reload
    ↓
Desktop Refresh
    ↓
Render
    ↓
Screenshot QA
    ↓
Scope/Git QA
    ↓
Final PASS


CORE RULE
---------

Never use:

"try something and see if it works."

Always use:

PLAN
→ IMPLEMENT
→ VALIDATE
→ CORRECT IF REQUIRED
→ ACCEPT
→ NEXT STEP


TOKEN EFFICIENCY
----------------

1. Read the plan once.
2. Read only the files required for the current task.
3. Do not repeatedly inspect unchanged files.
4. Validate the smallest possible scope first.
5. Use CLI validation instead of asking the model to reason about large JSON files.
6. Implement one visual at a time during HITL.
7. Stop immediately on failure.
8. Fix the smallest affected object.
9. Do not regenerate working pages.
10. Do not send full files into the model when targeted inspection is sufficient.