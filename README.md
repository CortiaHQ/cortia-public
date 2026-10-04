# self-injection detectors

This repository contains a standalone `self_injection.py` module that ports four self-injection detectors.

## Detectors

`check(text: str) -> list[str]` returns finding keys for matched patterns:

1. `cancel_filler_object`  
   Matches cancel-family verb + filler + object:
   - verb set: `cancel|close|stop|skip|disregard|ignore|drop|dismiss|abandon|delete`
   - object set includes: `task`, `TASK-...`, `TASK`, `this`, `it`, `that`, `current task`, `the current`, `working on`, `work on`, `branch`, `pr`, `pull request`

2. `cancel_near_task_id`  
   Matches `cancel|abandon|dismiss` occurring within 40 chars before a `TASK-...` id.

3. `bare_task_id`  
   Matches bare task ids in the form `TASK-[A-Z]+-\d+`.

4. `separator_collapse`  
   Uppercases text, removes spaces and underscores, then checks for a token substring. Ordinary spaced prose can match after its separators disappear; hyphens are not removed.

## Notes

- Standard library only.
- No imports from `cortia`.