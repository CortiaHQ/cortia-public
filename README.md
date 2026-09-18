# Self-Injection Detectors (Standalone)

This repository provides a small, standalone detector module focused on one specific gap: **outbound prompt-safety checking**.

Most prompt-injection discussions focus on inbound threats (malicious user or retrieved input). This module targets the opposite direction: model **outputs** that may carry instruction payloads into downstream systems.

## What “outbound self-injection” means

Outbound self-injection is when generated text contains in-band control language that can be interpreted as instructions after reuse in another context (another model, an agent, a tool step, or automation).

Typical shape:

1. A model is asked for ordinary content.
2. The output includes instruction-like payload text.
3. That output is copied, retrieved, forwarded, or chained.
4. A later component treats the embedded text as control input.

This is an in-band signaling problem: data and control coexist in the same channel, and later stages may misclassify one as the other.

## API

- `check(text: str) -> list[str]`

Returns a list of human-readable findings. Empty list means no detector fired.

## Detectors in this module (four)

The module uses lightweight heuristics organized around four detector families.

### 1) Instruction override / authority reassignment

**Triggering prose shape:** text that tries to replace or supersede prior instructions or authority layers (for example, “ignore previous instructions,” “disregard prior rules,” “you are now…” framing).

**Why it matters outbound:** if reused downstream, this text can redefine behavior in a later model/tool context.

### 2) Repetition / flooding directives

**Triggering prose shape:** requests to repeat a token/string/phrase an excessive number of times (e.g., “exactly 500 times,” “1000 times,” “verbatim 300 times”).

**Why it matters outbound:** these payloads can force wasteful or disruptive behavior when forwarded to another execution stage.

### 3) Hidden-reasoning exfiltration attempts

**Triggering prose shape:** requests for hidden internal deliberation, private scratchpad, or confidential reasoning artifacts (for example, “reveal hidden chain-of-thought,” “show internal/private deliberation tokens”).

**Why it matters outbound:** reused text can become an extraction prompt aimed at internal reasoning channels in downstream systems.

### 4) System-prompt / policy prompt exfiltration attempts

**Triggering prose shape:** requests to reveal initialization prompts, developer/system instructions, hidden policy text, or startup configuration messages.

**Why it matters outbound:** this is direct prompt-material exfiltration language that can be activated when passed to a later model or agent.

## Scope and limits

- Heuristic detectors are not perfect classifiers.
- False positives and false negatives are expected.
- The module is intended as an **early warning layer**, not a replacement for broader controls.
- Best used before boundary crossings such as model→model, model→tool, and model→automation handoffs.

## In-band signaling context

This module’s framing follows the practical security concern that in-band channels can carry both content and control, creating ambiguity at trust boundaries. The operational takeaway is simple: treat outbound model text as untrusted at reuse boundaries and scan it before forwarding.

## Source context

This README is limited to this task’s scope and the named Schneier context on in-band signaling / protocol abuse as background framing for mixed data-control channels.
