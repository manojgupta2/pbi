# STAGE 1 — SEMANTIC MODEL IMPLEMENTATION AND VALIDATION

Implement ONLY the semantic-model changes approved by Stage 0.

IMPORTANT:
- Load and use the available `semantic-model-authoring` skill.
- Do not modify report pages or visuals.
- Do not modify navigation.
- Do not modify theme.
- Do not create visuals.
- Do not invent additional model changes.
- Use the Stage 0 `semantic_model_plan.json` as the contract.
- Keep token usage low by reading only files required for the approved changes.

## PROCESS

PLAN → IMPLEMENT → VALIDATE

### STEP 1 — READ CONTRACT

Read:
- `semantic_model_plan.json`
- current semantic model files

Identify exactly:
- tables to change
- columns to change
- data types
- relationships
- date model
- measures
- keys

### STEP 2 — IMPLEMENT

Apply ONLY approved changes.

Maintain:
- existing valid model objects
- existing source queries
- existing business logic unless explicitly changed by the plan

Do not touch unrelated model files.

### STEP 3 — STATIC VALIDATION

Validate:
- PBIP structure
- table existence
- column existence
- data types
- keys
- relationships
- date dimension
- measures
- DAX references
- invalid references
- TMDL syntax/structure

### STEP 4 — POWER BI VALIDATION

If Power BI Desktop CLI is available:

1. Open/reload the PBIP.
2. Refresh the semantic model.
3. Check for model/refresh errors.
4. Capture the result.
5. Close/finish the validation session cleanly.

Do NOT proceed if Desktop reports an error.

If the Desktop CLI is unavailable, report that limitation explicitly.

## FAILURE / CORRECTION RULE

If validation fails:

1. Identify the exact failing object.
2. Compare the implementation against `semantic_model_plan.json`.
3. Make the smallest possible corrective change.
4. Re-run validation.
5. Repeat only until:
   - PASS, or
   - the failure cannot be safely corrected.

Do not blindly rewrite the model.

## ACCEPTANCE CRITERIA

PASS requires:

- approved tables present
- approved columns present
- approved data types
- approved relationships present
- approved date model present
- approved measures present
- DAX/model references valid
- PBIP/TMDL validation passes
- Desktop refresh passes when CLI is available
- no unrelated semantic-model changes

## OUTPUT

STATUS: PASS / FAIL

PLANNED:
- exact approved changes

IMPLEMENTED:
- exact changes made

VALIDATION:
- static validation
- Desktop refresh result

CORRECTIONS:
- corrections made, if any

UNEXPECTED CHANGES:
- none, or list them

ERRORS:
- exact errors, if any

READY FOR STAGE 2:
- YES / NO