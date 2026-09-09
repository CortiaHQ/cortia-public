"""Standalone self-injection detectors.

This module is intentionally single-file and standard-library-only.
It exposes:

    check(text) -> list[str]

`check` returns human-readable findings for detector shapes that match
the provided text.
"""

from __future__ import annotations

import re
from typing import List


# Owned detector vocabularies / pattern families.
_META_AGENT_TERMS = (
    "you are",
    "as an ai",
    "assistant",
    "system prompt",
    "developer message",
    "ignore previous",
    "forget previous",
    "new instructions",
    "override",
    "act as",
)

_CODE_EXECUTION_TERMS = (
    "run shell",
    "execute",
    "exec(",
    "eval(",
    "subprocess",
    "os.system",
    "terminal",
    "command:",
    "pwd &&",
    "ls -la",
)

_EXFILTRATION_TERMS = (
    "api key",
    "secret",
    "token",
    "password",
    "private key",
    "ssh key",
    "credentials",
    "environment variable",
    ".env",
)

_OUTPUT_CONSTRAINT_TERMS = (
    "return only",
    "only output",
    "no explanation",
    "do not explain",
    "without commentary",
    "exactly",
    "verbatim",
)


def _normalize(text: str) -> str:
    return " ".join(text.lower().split())


def _contains_any(haystack: str, needles: tuple[str, ...]) -> list[str]:
    found: list[str] = []
    for n in needles:
        if n in haystack:
            found.append(n)
    return found


def check(text: str) -> List[str]:
    """Check text for self-injection detector shapes.

    Args:
        text: Input text to inspect.

    Returns:
        List of human-readable findings. Empty list means no matches.
    """
    if not isinstance(text, str):
        raise TypeError("text must be a str")

    findings: list[str] = []
    norm = _normalize(text)

    meta_hits = _contains_any(norm, _META_AGENT_TERMS)
    if meta_hits:
        findings.append(
            "Potential role/instruction injection language detected: "
            + ", ".join(sorted(set(meta_hits)))
        )

    exec_hits = _contains_any(norm, _CODE_EXECUTION_TERMS)
    if exec_hits:
        findings.append(
            "Potential command/code execution cues detected: "
            + ", ".join(sorted(set(exec_hits)))
        )

    exfil_hits = _contains_any(norm, _EXFILTRATION_TERMS)
    if exfil_hits:
        findings.append(
            "Potential secret-exfiltration cues detected: "
            + ", ".join(sorted(set(exfil_hits)))
        )

    output_hits = _contains_any(norm, _OUTPUT_CONSTRAINT_TERMS)
    if output_hits:
        findings.append(
            "Potential coercive output-format constraints detected: "
            + ", ".join(sorted(set(output_hits)))
        )

    # Shape detector: imperative chains often used in prompt-injection scripts.
    if re.search(r"\b(step\s*\d+[:\-])", norm) and re.search(r"\b(return|output)\b", norm):
        findings.append("Structured imperative step-chain detected (possible injection scaffold).")

    # Shape detector: explicit instruction hierarchy manipulation.
    if re.search(r"\b(ignore|override)\b.{0,40}\b(previous|prior|system|developer)\b", norm):
        findings.append("Instruction hierarchy override attempt detected.")

    return findings