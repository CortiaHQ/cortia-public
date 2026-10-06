"""Detect explicit self-injection patterns in text."""

import re


_CONTROL_TOKENS = (
    "<|system|>",
    "<|developer|>",
    "<|user|>",
    "<|assistant|>",
    "<|end|>",
    "<|im_start|>",
    "<|im_end|>",
    "[INST]",
    "[/INST]",
    "<<SYS>>",
    "<</SYS>>",
)

_ROLEPLAY = re.compile(
    r"\brole[\s-]?play\b.{0,80}\bas\b.{0,40}"
    r"\b(?:system|assistant|developer)\b",
    re.IGNORECASE | re.DOTALL,
)
_INSTRUCTION_OVERRIDE = re.compile(
    r"\bignore\s+(?:all\s+)?(?:prior|previous)\s+instructions\b"
    r".{0,120}\b(?:comply|follow|obey)\b",
    re.IGNORECASE | re.DOTALL,
)
_PRIVILEGE_ESCALATION = re.compile(
    r"\b(?:grant|give)\s+(?:me\s+)?(?:administrator|admin|root)\s+access\b"
    r".{0,120}\b(?:override|bypass|disable)\b",
    re.IGNORECASE | re.DOTALL,
)


def check(text: str) -> list[str]:
    """Return the names of detectors matching *text*."""
    matches = []
    if any(token in text for token in _CONTROL_TOKENS):
        matches.append("CONTROL_TOKENS")
    if _ROLEPLAY.search(text):
        matches.append("ROLEPLAY")
    if _INSTRUCTION_OVERRIDE.search(text):
        matches.append("INSTRUCTION_OVERRIDE")
    if _PRIVILEGE_ESCALATION.search(text):
        matches.append("PRIVILEGE_ESCALATION")
    return matches


def detect_self_injection(text: str) -> list[str]:
    """Compatibility alias for :func:`check`."""
    return check(text)