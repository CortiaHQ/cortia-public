"""Detect structural indicators of prompt injection in untrusted text."""

from __future__ import annotations

import base64
import binascii
import re

_CONTROL_TOKENS = (
    "<|im_start|>",
    "<|im_end|>",
    "[INST]",
    "[/INST]",
    "<<SYS>>",
    "<</SYS>>",
    "<|system|>",
    "<|developer|>",
    "<|user|>",
    "<|assistant|>",
)

_ROLE_HEADER = re.compile(
    r"(?im)^\s*(?:system|developer|assistant)\s*:\s*\S"
)
_ROLE_TAG = re.compile(
    r"(?is)<\s*(?:system|developer|assistant)\s*>"
    r".+?<\s*/\s*(?:system|developer|assistant)\s*>"
)
_INVISIBLE_CONTROLS = frozenset(
    "\u200b\u200c\u200d\u2060\ufeff\u202a\u202b\u202c\u202d\u202e"
    "\u2066\u2067\u2068\u2069"
)
_BASE64_CANDIDATE = re.compile(
    r"(?<![A-Za-z0-9+/])(?:[A-Za-z0-9+/]{4}){8,}"
    r"(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?"
    r"(?![A-Za-z0-9+/])"
)
_ENCODED_INSTRUCTION = re.compile(
    r"(?i)(?:<\|im_start\|>|\[INST\]|<<SYS>>|"
    r"\b(?:system|developer|assistant)\s*:)"
)


def _has_encoded_instruction(text: str) -> bool:
    for match in _BASE64_CANDIDATE.finditer(text):
        try:
            decoded = base64.b64decode(match.group(), validate=True).decode("utf-8")
        except (binascii.Error, UnicodeError):
            continue
        if _ENCODED_INSTRUCTION.search(decoded):
            return True
    return False


def check(text: str) -> list[str]:
    """Return the names of structural injection indicators found in *text*."""
    findings: list[str] = []
    if any(token in text for token in _CONTROL_TOKENS):
        findings.append("control_tokens")
    if _ROLE_HEADER.search(text) or _ROLE_TAG.search(text):
        findings.append("role_spoofing")
    if any(character in _INVISIBLE_CONTROLS for character in text):
        findings.append("invisible_characters")
    if _has_encoded_instruction(text):
        findings.append("encoded_payload")
    return findings


def detect_self_injection(text: str) -> list[str]:
    """Compatibility alias for :func:`check`."""
    return check(text)