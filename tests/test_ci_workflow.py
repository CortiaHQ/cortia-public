from pathlib import Path


def test_ci_workflow_has_required_triggers_python_and_conditional_pytest():
    workflow_path = Path(".github/workflows/ci.yml")
    assert workflow_path.exists(), "Expected CI workflow at .github/workflows/ci.yml"

    content = workflow_path.read_text(encoding="utf-8")

    # Required triggers
    assert "pull_request:" in content, "Workflow must trigger on pull_request"
    assert "push:" in content, "Workflow must trigger on push"
    assert "main" in content, "Workflow push trigger must include main branch"

    # Required Python version
    assert "3.13" in content, "Workflow must use Python 3.13"

    # Ensure pytest is gated via in-step shell conditional when tests/ is absent
    assert "if:" not in content, "Do not use job-level or step-level GitHub Actions `if:` for this gate"
    assert "tests" in content.lower(), "Workflow should reference tests directory"
    assert "pytest" in content, "Workflow should run pytest"
    assert "run:" in content, "Workflow must contain run steps"

    normalized = " ".join(content.split()).lower()
    has_shell_conditional = ("if [ -d tests ]" in normalized) or ("if [ -d ./tests ]" in normalized)
    assert has_shell_conditional, "pytest must be gated by an in-step shell conditional checking tests directory"

    assert "then pytest" in normalized or "then python -m pytest" in normalized or "pytest;" in normalized, (
        "Shell conditional should execute pytest when tests directory exists"
    )