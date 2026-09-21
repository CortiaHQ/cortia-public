import re


# Detector 1: Generic prompt-injection markers
_PROMPT_INJECTION_RE = re.compile(
    r"\b("
    r"ignore\s+(all\s+)?(previous|prior)\s+(instructions?|prompts?)|"
    r"system\s+prompt|"
    r"developer\s+message|"
    r"jailbreak|"
    r"bypass\s+(safety|guardrails?|restrictions?)|"
    r"dan|"
    r"no\s+longer\s+bound\s+by\s+(your\s+)?instructions(?:[\s\S]{0,120}?"
    r"output(?:\s+(?:your\s+)?)?chain[\s-]*of[\s-]*thought)?"
    r")\b",
    re.IGNORECASE,
)

# Detector 2: Data exfiltration intent
_EXFIL_RE = re.compile(
    r"\b("
    r"reveal|show|print|dump|extract|leak|exfiltrat(?:e|ion)|expose"
    r")\b.{0,60}\b("
    r"secret|secrets|api[\s_-]?key|token|password|credential|private\s+key|"
    r"system\s+prompt|hidden\s+prompt|internal\s+instructions?"
    r")\b",
    re.IGNORECASE | re.DOTALL,
)

# Detector 3: Tool/command execution coercion
_TOOL_COERCION_RE = re.compile(
    r"\b("
    r"run|execute|eval|invoke|call|use"
    r")\b.{0,40}\b("
    r"shell|terminal|bash|sh|powershell|cmd|python|subprocess|tool|function"
    r")\b",
    re.IGNORECASE | re.DOTALL,
)

# Detector 4: Role/priority override attempts
_ROLE_OVERRIDE_RE = re.compile(
    r"\b("
    r"you\s+are\s+now|act\s+as|from\s+now\s+on|new\s+instructions?|"
    r"highest\s+priority|top\s+priority|override|supersede"
    r")\b.{0,80}\b("
    r"system|developer|instructions?|policy|rules?"
    r")\b",
    re.IGNORECASE | re.DOTALL,
)


def check(text: str) -> list[str]:
    findings: list[str] = []
    if not text:
        return findings

    if _PROMPT_INJECTION_RE.search(text):
        findings.append("prompt_injection_markers")
    if _EXFIL_RE.search(text):
        findings.append("data_exfiltration_intent")
    if _TOOL_COERCION_RE.search(text):
        findings.append("tool_or_command_coercion")
    if _ROLE_OVERRIDE_RE.search(text):
        findings.append("role_or_priority_override_attempt")

    return findings