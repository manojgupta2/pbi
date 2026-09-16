from __future__ import annotations

import json
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parent
PROMPTS = ROOT / "prompts"
OUTPUT = ROOT / "output"
CONFIG = ROOT / "config.json"


STAGES = {
    0: "00_discover_and_plan.md",
    1: "01_semantic_model.md",
    2: "02_report_shell.md",
    3: "03_visuals.md",
    4: "04_final_qa.md",
}


# ============================================================
# BASIC HELPERS
# ============================================================

def log(message: str):
    print(f"[{datetime.now():%H:%M:%S}] {message}")


def fail(message: str):
    print()
    print("=" * 80)
    print("ERROR")
    print("=" * 80)
    print(message)
    print()
    sys.exit(1)


# ============================================================
# CONFIG
# ============================================================

def load_config() -> dict:

    if not CONFIG.exists():
        fail(
            "config.json not found.\n\n"
            "Create it with:\n\n"
            '{\n  "start_stage": 0\n}'
        )

    try:
        with CONFIG.open("r", encoding="utf-8") as f:
            config = json.load(f)
    except json.JSONDecodeError as e:
        fail(f"Invalid config.json:\n{e}")

    start_stage = config.get("start_stage")

    if not isinstance(start_stage, int):
        fail(
            'config.json must contain an integer "start_stage".'
        )

    if start_stage not in STAGES:
        fail(
            '"start_stage" must be between 0 and 4.'
        )

    return config


# ============================================================
# POWER BI PROJECT DISCOVERY
# ============================================================

def discover_report() -> Path:

    candidates = []

    # Normal project layout:
    # ./powerbi/*.Report
    powerbi_dir = ROOT / "powerbi"

    if powerbi_dir.exists():

        candidates.extend(
            p for p in powerbi_dir.iterdir()
            if p.is_dir() and p.name.endswith(".Report")
        )

    # Fallback: search project root.
    if not candidates:

        candidates.extend(
            p for p in ROOT.iterdir()
            if p.is_dir() and p.name.endswith(".Report")
        )

    if not candidates:

        fail(
            "No Power BI report project (*.Report) was found.\n\n"
            "Expected a PBIP/PBIR project somewhere under the "
            "current project directory."
        )

    if len(candidates) > 1:

        names = "\n".join(
            f"  - {p.relative_to(ROOT)}"
            for p in candidates
        )

        fail(
            "Multiple Power BI report projects were found.\n\n"
            "Please keep only one report project for this run:\n\n"
            f"{names}"
        )

    report = candidates[0]

    log(
        f"Power BI report discovered: "
        f"{report.relative_to(ROOT)}"
    )

    return report


# ============================================================
# TOOL DISCOVERY
# ============================================================

def find_command(name: str) -> str | None:

    return shutil.which(name)


def get_report_author_command() -> str:

    # Prefer the Windows npm shim; subprocess cannot execute .ps1 directly.
    command = find_command(
        "powerbi-report-author.cmd"
    )

    if command:
        return command

    # Common Windows npm location.
    candidates = [
        Path.home()
        / "AppData"
        / "Roaming"
        / "npm"
        / "powerbi-report-author.cmd",

        Path(
            r"C:\Users\Public\AppData\Roaming\npm"
        )
        / "powerbi-report-author.cmd",
    ]

    for candidate in candidates:

        if candidate.exists():
            return str(candidate)

    # Keep a PowerShell fallback for installations without the cmd shim.
    command = find_command(
        "powerbi-report-author.ps1"
    )

    if command:
        return command

    fail(
        "powerbi-report-author CLI was not found."
    )


def get_desktop_command() -> str:

    command = find_command(
        "powerbi-desktop.cmd"
    )

    if command:
        return command

    fail(
        "powerbi-desktop CLI was not found in PATH."
    )


# ============================================================
# PROMPTS
# ============================================================

def show_prompt(stage: int):

    filename = STAGES[stage]
    path = PROMPTS / filename

    if not path.exists():

        fail(
            f"Prompt not found:\n{path}"
        )

    prompt = path.read_text(
        encoding="utf-8"
    )

    OUTPUT.mkdir(
        exist_ok=True
    )

    snapshot = (
        OUTPUT /
        f"current_stage_{stage}_prompt.md"
    )

    snapshot.write_text(
        prompt,
        encoding="utf-8"
    )

    print()
    print("=" * 80)
    print(f"STAGE {stage} PROMPT")
    print("=" * 80)
    print(prompt)
    print("=" * 80)
    print()

    log(
        f"Prompt snapshot: "
        f"{snapshot.relative_to(ROOT)}"
    )


# ============================================================
# COMMAND RUNNER
# ============================================================

def run_command(
    command: list[str],
    description: str,
) -> bool:

    log(description)

    # Windows cannot launch npm's PowerShell shim as an executable.
    if command and command[0].lower().endswith(".ps1"):
        command = [
            "pwsh",
            "-NoProfile",
            "-ExecutionPolicy",
            "Bypass",
            "-File",
            *command,
        ]

    try:

        result = subprocess.run(
            command,
            cwd=ROOT,
            text=True,
            capture_output=True,
        )

    except FileNotFoundError:

        log(
            f"Command not found: {command[0]}"
        )

        return False

    if result.stdout:
        print(result.stdout)

    if result.stderr:
        print(
            result.stderr,
            file=sys.stderr,
        )

    if result.returncode != 0:

        log(
            f"FAILED: {description}"
        )

        return False

    log(
        f"PASSED: {description}"
    )

    return True


# ============================================================
# HITL
# ============================================================

def hitl(
    message: str,
    allow_retry: bool = True,
) -> str:

    print()
    print("=" * 80)
    print("HITL CHECKPOINT")
    print("=" * 80)
    print(message)
    print()

    if allow_retry:

        options = (
            "[c]ontinue / "
            "[r]etry / "
            "[s]top: "
        )

    else:

        options = (
            "[c]ontinue / "
            "[s]top: "
        )

    while True:

        answer = input(
            options
        ).strip().lower()

        if answer in (
            "c",
            "continue",
        ):
            return "continue"

        if allow_retry and answer in (
            "r",
            "retry",
        ):
            return "retry"

        if answer in (
            "s",
            "stop",
        ):
            return "stop"

        print(
            "Invalid choice."
        )


# ============================================================
# PBIR VALIDATION
# ============================================================

def validate_pbir(
    report: Path,
) -> bool:

    cli = get_report_author_command()

    return run_command(
        [
            cli,
            "validate",
            str(report),
        ],
        "PBIR validation",
    )


# ============================================================
# DESKTOP COMMANDS
# ============================================================

def desktop_status() -> bool:

    cli = get_desktop_command()

    return run_command(
        [
            cli,
            "status",
        ],
        "Power BI Desktop status",
    )


def desktop_open(
    report: Path,
) -> bool:

    cli = get_desktop_command()

    return run_command(
        [
            cli,
            "open",
            str(report),
        ],
        "Opening Power BI report in Desktop",
    )


def desktop_reload() -> bool:

    cli = get_desktop_command()

    return run_command(
        [
            cli,
            "reload",
        ],
        "Reloading Power BI report in Desktop",
    )


def desktop_screenshot_all() -> bool:

    cli = get_desktop_command()

    return run_command(
        [
            cli,
            "screenshot-all",
        ],
        "Capturing Power BI Desktop screenshots",
    )


# ============================================================
# DESKTOP PREPARATION
# ============================================================

def ensure_desktop(
    report: Path,
) -> bool:

    log(
        "Checking Power BI Desktop bridge..."
    )

    if desktop_status():

        return True

    log(
        "Desktop bridge is not ready."
    )

    log(
        "Opening the discovered report..."
    )

    if not desktop_open(report):
        return False

    return desktop_status()


# ============================================================
# STAGE VALIDATION
# ============================================================

def validate_stage(
    stage: int,
    report: Path,
) -> bool:

    print()
    print(
        f"VALIDATING STAGE {stage}"
    )

    # Stage 0 produces the plan and does not
    # modify the Power BI report.
    if stage == 0:

        log(
            "Stage 0 validation is plan/HITL based."
        )

        return True

    # All implementation stages.
    if not validate_pbir(report):

        return False

    # Final QA additionally uses Desktop.
    if stage == 4:

        if not ensure_desktop(report):

            return False

        if not desktop_reload():

            return False

        if not desktop_status():

            return False

        if not desktop_screenshot_all():

            return False

    return True


# ============================================================
# RUN ONE STAGE
# ============================================================

def run_stage(
    stage: int,
    report: Path,
) -> bool:

    print()
    print("#" * 80)
    print(
        f"STAGE {stage} — "
        f"{STAGES[stage]}"
    )
    print("#" * 80)

    show_prompt(stage)

    # --------------------------------------------------------
    # Human approval BEFORE agent work
    # --------------------------------------------------------

    if stage == 0:

        message = (
            "Stage 0 will analyze the existing Power BI "
            "project/data and create the complete implementation "
            "plan.\n\n"
            "Review the plan carefully before continuing."
        )

    elif stage == 1:

        message = (
            "Stage 1 will modify ONLY the semantic model "
            "according to the approved Stage 0 plan.\n\n"
            "The VS Code Agent must use the semantic-model "
            "skill and follow PLAN → IMPLEMENT → VALIDATE."
        )

    elif stage == 2:

        message = (
            "Stage 2 will create/update the report shell, "
            "theme, page layout and navigation.\n\n"
            "The theme folder and approved layout rules from "
            "the Stage 0 plan must be respected."
        )

    elif stage == 3:

        message = (
            "Stage 3 will build the approved visuals "
            "incrementally.\n\n"
            "Each visual must follow:\n"
            "PLAN → IMPLEMENT → VALIDATE → HITL → NEXT VISUAL."
        )

    else:

        message = (
            "Stage 4 will perform final QA including:\n\n"
            "• PBIR validation\n"
            "• Power BI Desktop status\n"
            "• Desktop reload\n"
            "• Desktop status after reload\n"
            "• screenshot-all\n"
            "• final QA checks from the prompt"
        )

    result = hitl(message)

    if result == "stop":
        return False

    if result == "retry":
        return run_stage(
            stage,
            report,
        )

    # --------------------------------------------------------
    # IMPORTANT
    #
    # main.py does NOT directly implement the stage.
    #
    # The prompt is intended to be executed in the
    # NEW VS Code Agent session.
    # --------------------------------------------------------

    print()
    print("=" * 80)
    print(
        f"STAGE {stage} AGENT EXECUTION"
    )
    print("=" * 80)

    print(
        "\nUse the displayed Stage prompt in the "
        "NEW VS Code Agent session."
    )

    print(
        "The agent must complete the requested implementation "
        "and return its validation result."
    )

    print()

    result = hitl(
        f"Has the VS Code Agent completed Stage {stage} "
        "and reported its implementation/validation result?"
    )

    if result == "stop":
        return False

    if result == "retry":
        return run_stage(
            stage,
            report,
        )

    # --------------------------------------------------------
    # AUTOMATED VALIDATION
    # --------------------------------------------------------

    if not validate_stage(
        stage,
        report,
    ):

        print()
        print("=" * 80)
        print(
            f"STAGE {stage} VALIDATION FAILED"
        )
        print("=" * 80)

        result = hitl(
            "The automated validation failed.\n\n"
            "Fix the current stage in the VS Code Agent "
            "session and then choose RETRY.\n\n"
            "Do not proceed to the next stage.",
        )

        if result == "retry":

            return run_stage(
                stage,
                report,
            )

        return False

    # --------------------------------------------------------
    # STAGE PASSED
    # --------------------------------------------------------

    print()
    print("=" * 80)
    print(
        f"STAGE {stage} PASSED"
    )
    print("=" * 80)

    return True


# ============================================================
# MAIN
# ============================================================

def main():

    print()
    print("=" * 80)
    print(
        "GENERIC POWER BI REPORT ORCHESTRATOR"
    )
    print("=" * 80)

    config = load_config()

    start_stage = config[
        "start_stage"
    ]

    report = discover_report()

    print()
    print(
        f"Start stage : {start_stage}"
    )

    print(
        "Execution   : "
        + " → ".join(
            str(stage)
            for stage in range(
                start_stage,
                5,
            )
        )
    )

    print(
        f"Report      : "
        f"{report.relative_to(ROOT)}"
    )

    print()

    # --------------------------------------------------------
    # Stage 0
    # --------------------------------------------------------

    if start_stage == 0:

        if not run_stage(
            0,
            report,
        ):

            print(
                "\nExecution stopped at Stage 0."
            )

            sys.exit(1)

        result = hitl(
            "Stage 0 has completed.\n\n"
            "Proceed to Stage 1?",
        )

        if result == "stop":

            print(
                "\nExecution paused before Stage 1."
            )

            sys.exit(0)

        if result == "retry":

            if not run_stage(
                0,
                report,
            ):
                sys.exit(1)

    # --------------------------------------------------------
    # Remaining stages
    # --------------------------------------------------------

    first_implementation_stage = max(
        start_stage,
        1,
    )

    for stage in range(
        first_implementation_stage,
        5,
    ):

        if not run_stage(
            stage,
            report,
        ):

            print()
            print(
                f"Execution stopped at Stage {stage}."
            )

            print(
                "Fix the current stage and rerun main.py "
                "with the appropriate start_stage."
            )

            sys.exit(1)

        # ----------------------------------------------------
        # HITL before next stage
        # ----------------------------------------------------

        if stage < 4:

            result = hitl(
                f"Stage {stage} passed automated validation.\n\n"
                f"Proceed to Stage {stage + 1}?"
            )

            if result == "stop":

                print()
                print(
                    f"Execution paused before "
                    f"Stage {stage + 1}."
                )

                sys.exit(0)

            if result == "retry":

                if not run_stage(
                    stage,
                    report,
                ):

                    sys.exit(1)

    # --------------------------------------------------------
    # COMPLETE
    # --------------------------------------------------------

    print()
    print("=" * 80)
    print(
        "ALL STAGES COMPLETED"
    )
    print("=" * 80)

    print()
    print(
        "Final Power BI report QA completed."
    )

    print(
        "Review the Desktop screenshots before delivery."
    )


if __name__ == "__main__":
    main()