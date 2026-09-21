# TASK-GH-2971: Detector README

This repository documents four detectors used to identify suspicious trigger patterns and the in-band signaling framing they rely on.

## Overview

The detectors are shape-based checks over observed trigger activity. They do not infer intent; they flag pattern forms that may warrant review. The underlying concept is **in-band signaling**: a sender and receiver can coordinate using the same channel as normal traffic, embedding meaning in timing, structure, or distribution rather than explicit out-of-band metadata.

## The Four Detectors

### 1) Burst Detector
**Trigger shape:** a sharp, short-lived spike in trigger frequency relative to local baseline.

- Looks for abrupt concentration of events in a narrow window.
- Useful for spotting “flash” signaling where meaning is encoded by sudden intensity.
- Typical visual shape: low/steady background, then a steep peak, then return to baseline.

### 2) Stair-Step Detector
**Trigger shape:** monotonic, staged increases (or decreases) across adjacent windows.

- Flags sequences that rise/fall in deliberate-looking increments.
- Useful for signaling schemes that encode state through level transitions.
- Typical visual shape: plateaus connected by step changes rather than random jitter.

### 3) Pulse-Train Detector
**Trigger shape:** repeated pulses with roughly consistent spacing and width.

- Identifies periodic or quasi-periodic on/off activity.
- Useful where cadence itself carries information.
- Typical visual shape: multiple peaks separated by near-regular intervals.

### 4) Edge-Pair Detector
**Trigger shape:** paired transitions (start/stop, high/low, on/off) with constrained gap patterns.

- Detects boundary-encoded signaling where information is in edges and their separations.
- Useful when absolute volume is low but transition timing is structured.
- Typical visual shape: recurring edge couples with similar inter-edge distance.

## In-Band Signaling Framing

All four detectors are framed as **in-band signaling** detectors:

- The same operational channel carries both ordinary activity and potential signal.
- The signal is represented by pattern shape (burst, steps, cadence, edge gaps), not separate control fields.
- Detection is therefore pattern-analytic, focusing on temporal/structural regularity over content semantics.

## Citation

Conceptual framing reference:

- Bruce Schneier, “AI and Invisible Manipulation,” 13 May 2024.