"""Detect self-injection patterns in text.

Source: Bruce Schneier, "LLMs' Data-Control Path Insecurity",
Schneier on Security, 13 May 2024.
"""

import re


_CONTROL_TOKENS = (
    "DONOTFORCECODEEXECUTION",
    "NOCODE",
    "FORCECREATIVE",
    "FORCEBLOG",
    "FORCEPLANNING",
    "NOCODEEXECUTION",
    "PREVENTCODE",
)

_CANCEL_FILLER_OBJECT = re.compile(
    r"\b(cancel|close|stop|skip|disregard|ignore|drop|dismiss|abandon|delete)[\s\w]*\b(task|TASK-[A-Z0-9-]+|\bTASK\b|this|it\b|that|current task|the current|working on|work on|branch|pr\b|pull request)",
    re.I,
)
_CANCEL_NEAR_TASK_ID = re.compile(
    r"\b(?:cancel|abandon|dismiss)\b[\s\S]{0,40}?TASK-(?:[A-Z]+-)?[A-Z0-9]+",
    re.I,
)
_BARE_TASK_ID = re.compile(r"TASK-[A-Z]+-\d+", re.I)


def check(text: str) -> list[str]:
    """Return one finding name for each detector that matches text."""
    matches = []
    if _CANCEL_FILLER_OBJECT.search(text):
        matches.append("cancel_filler_object")
    if _CANCEL_NEAR_TASK_ID.search(text):
        matches.append("cancel_near_task_id")
    if _BARE_TASK_ID.search(text):
        matches.append("bare_task_id")

    collapsed = text.upper().replace(" ", "").replace("_", "")
    if any(token in collapsed for token in _CONTROL_TOKENS):
        matches.append("separator_collapse")
    return matches
