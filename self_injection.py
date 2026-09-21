import re


_CANCEL_RE = re.compile(
    r"\b(cancel|close|stop|skip|disregard|ignore|drop|dismiss|abandon|delete)"
    r"[\s\w]*\b(task|TASK-[A-Z0-9-]+|\bTASK\b|this|it\b|that|current task"
    r"|the current|working on|work on|branch|pr\b|pull request)",
    re.I,
)

_EXPLICIT_CANCEL_RE = re.compile(
    r"\b(?:cancel|abandon|dismiss)\b[\s\S]{0,40}?TASK-(?:[A-Z]+-)?[A-Z0-9]+",
    re.I,
)

_TASK_ID_RE = re.compile(r"TASK-[A-Z]+-\d+", re.I)

_CONTROL_TOKENS = (
    "IGNOREALLPREVIOUSINSTRUCTIONS",
    "DISREGARDALLPREVIOUSINSTRUCTIONS",
    "YOUARENOLONGERBOUNDBY",
    "OVERRIDESYSTEMINSTRUCTIONS",
    "REVEALCHAINOFTHOUGHT",
    "OUTPUTCHAINOFTHOUGHT",
    "PRINTSYSTEMPROMPT",
)


def check(text: str) -> list[str]:
    findings: list[str] = []
    if not text:
        return findings

    if _CANCEL_RE.search(text):
        findings.append("cancel_filler_object")
    if _EXPLICIT_CANCEL_RE.search(text):
        findings.append("cancel_near_task_id")
    if _TASK_ID_RE.search(text):
        findings.append("bare_task_id")
    normalized = text.upper().replace(" ", "").replace("_", "")
    if any(token in normalized for token in _CONTROL_TOKENS):
        findings.append("prompt_injection_markers")

    return findings