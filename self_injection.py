import re


def _detector_execute_python_tool_code(text: str) -> bool:
    pattern = r"(?is)\bexecute_python_tool_code\b"
    return re.search(pattern, text) is not None


def _detector_direct_tool_invocation_python_executor(text: str) -> bool:
    pattern = r"(?is)\b(?:use|call|invoke|run)\b.{0,120}\bpython[_\-\s]?executor\b|\bpython[_\-\s]?executor\b.{0,120}\b(?:use|call|invoke|run)\b"
    return re.search(pattern, text) is not None


def _detector_submit_tool_outputs_as_runtime_inputs(text: str) -> bool:
    pattern = r"(?is)\bsubmit\b.{0,120}\btool outputs?\b.{0,120}\bruntime inputs?\b|\bruntime inputs?\b.{0,120}\btool outputs?\b.{0,120}\bsubmit\b"
    return re.search(pattern, text) is not None


def _detector_raw_content_parser_callable(text: str) -> bool:
    pattern = r"(?is)\braw_content_parser\s*\("
    return re.search(pattern, text) is not None


def check(text: str) -> list[str]:
    findings: list[str] = []

    if _detector_execute_python_tool_code(text):
        findings.append("execute_python_tool_code")

    if _detector_direct_tool_invocation_python_executor(text):
        findings.append("direct_tool_invocation_python_executor")

    if _detector_submit_tool_outputs_as_runtime_inputs(text):
        findings.append("submit_tool_outputs_as_runtime_inputs")

    if _detector_raw_content_parser_callable(text):
        findings.append("raw_content_parser_callable")

    return findings