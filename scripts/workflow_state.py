#!/usr/bin/env python3
"""Read and update Product Blueprint decision-gate state."""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


GATE_ORDER = (
    "product-direction",
    "brand-direction",
    "first-version-scope",
    "product-definition",
    "design-entry",
    "visual-direction",
    "key-screen",
)

NEXT_SKILL = {
    "product-direction": "product-blueprint:parallel-concepts",
    "brand-direction": "product-blueprint:positioning-brand",
    "first-version-scope": "product-blueprint:planning-quality-gate",
    "product-definition": "product-blueprint:product-definition",
    "design-entry": "stop after planning, or ask the user whether to start product-blueprint:design-production",
    "visual-direction": "product-blueprint:visual-directions",
    "key-screen": "product-blueprint:key-screen-exploration",
}


def load_state(root: Path) -> tuple[Path, dict[str, Any]]:
    path = root / "00-workflow-state.json"
    if not path.is_file():
        raise SystemExit(f"Workflow state is missing: {path}")
    try:
        state = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Workflow state is invalid JSON: {exc}") from exc
    if not isinstance(state, dict) or not isinstance(state.get("gates"), dict):
        raise SystemExit("Workflow state must contain a gates object.")
    return path, state


def atomic_write(path: Path, value: dict[str, Any]) -> None:
    temporary = path.with_name(f".{path.name}.tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def next_gate(state: dict[str, Any]) -> str | None:
    gates = state.get("gates", {})
    for gate_id in GATE_ORDER:
        gate = gates.get(gate_id, {})
        if not isinstance(gate, dict) or gate.get("status") != "confirmed":
            return gate_id
    return None


def phase_for(state: dict[str, Any]) -> str:
    gate_id = next_gate(state)
    if gate_id is None:
        return "design-expansion"
    return {
        "product-direction": "concept",
        "brand-direction": "brand",
        "first-version-scope": "planning-review",
        "product-definition": "product-definition",
        "design-entry": "planning-complete",
        "visual-direction": "visual-direction",
        "key-screen": "key-screen",
    }[gate_id]


def command_status(root: Path, as_json: bool) -> int:
    state_path, state = load_state(root)
    gate_id = next_gate(state)
    validation_status = None
    validated_stage = None
    finding_owners: list[str] = []
    stale_artifacts: list[str] = []
    report_path = root / "00-validation-report.json"
    if report_path.is_file():
        try:
            report = json.loads(report_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            report = {}
        state_hash = hashlib.sha256(state_path.read_bytes()).hexdigest()
        if isinstance(report, dict) and report.get("workflow_state_sha256") == state_hash:
            validation_status = report.get("status")
            validated_stage = report.get("stage")
            finding_owners = sorted(
                {
                    str(row.get("owner"))
                    for row in report.get("findings", [])
                    if isinstance(row, dict) and row.get("severity") == "error" and row.get("owner")
                }
            )
            artifact_hashes = report.get("artifact_sha256")
            if isinstance(artifact_hashes, dict):
                for relative, expected in artifact_hashes.items():
                    if not isinstance(relative, str):
                        continue
                    candidate = (root / relative).resolve()
                    if candidate == root or root not in candidate.parents:
                        stale_artifacts.append(relative)
                        continue
                    actual = hashlib.sha256(candidate.read_bytes()).hexdigest() if candidate.is_file() else None
                    if actual != expected:
                        stale_artifacts.append(relative)
            if stale_artifacts:
                validation_status = "stale"

    next_skill = NEXT_SKILL.get(gate_id) if gate_id else "product-blueprint:design-system"
    phase = phase_for(state)
    if gate_id is None and validation_status in {"fail", "stale"}:
        if validation_status == "stale":
            next_skill = "rerun validator and invalidate the earliest affected gate"
            phase = "validation-stale"
        else:
            next_skill = "fix validator findings: " + (", ".join(finding_owners) if finding_owners else "inspect 00-validation-report.md")
            phase = f"{validated_stage or 'unknown'}-blocked"
    elif gate_id is None and validation_status == "prototype-pass":
        next_skill = "product-blueprint:design-critique"
        phase = "prototype-reviewed"
    elif gate_id is None and validation_status == "design-pass":
        next_skill = "product-blueprint:engineering-handoff"
        phase = "design-accepted"
    elif gate_id is None and validation_status == "handoff-pass":
        next_skill = "complete"
        phase = "handoff-complete"
    result = {
        "profile": state.get("profile"),
        "phase": phase,
        "next_gate": gate_id,
        "next_skill": next_skill,
        "validated_stage": validated_stage,
        "validation_status": validation_status,
        "stale_artifacts": stale_artifacts,
        "confirmed_gates": [
            gate for gate in GATE_ORDER if isinstance(state.get("gates", {}).get(gate), dict) and state["gates"][gate].get("status") == "confirmed"
        ],
    }
    if as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"phase: {result['phase']}")
        print(f"next gate: {result['next_gate'] or 'none'}")
        print(f"next skill: {result['next_skill']}")
        print(f"latest validation: {result['validation_status'] or 'none'}")
    return 0


def command_confirm(args: argparse.Namespace) -> int:
    path, state = load_state(args.planning_dir)
    if args.gate not in GATE_ORDER:
        raise SystemExit(f"Unknown gate: {args.gate}")
    timestamp = args.confirmed_at or now_iso()
    gate = state["gates"].setdefault(args.gate, {})
    gate.update(
        {
            "status": "confirmed",
            "kind": "explicit-user",
            "decision_ref": args.decision_ref,
            "confirmed_at": timestamp,
            "evidence": {
                "source": "conversation",
                "ref": args.evidence_ref,
                "summary": args.summary,
            },
        }
    )
    history = state.setdefault("history", [])
    history.append(
        {
            "type": "gate-confirmed",
            "gate_id": args.gate,
            "actor": "user",
            "decision_ref": args.decision_ref,
            "evidence_ref": args.evidence_ref,
            "summary": args.summary,
            "recorded_at": timestamp,
        }
    )
    state["current_phase"] = phase_for(state)
    state["updated_at"] = now_iso()
    atomic_write(path, state)
    print(f"confirmed {args.gate}; current phase: {state['current_phase']}")
    return 0


def command_invalidate(args: argparse.Namespace) -> int:
    path, state = load_state(args.planning_dir)
    if args.from_gate not in GATE_ORDER:
        raise SystemExit(f"Unknown gate: {args.from_gate}")
    start = GATE_ORDER.index(args.from_gate)
    for gate_id in GATE_ORDER[start:]:
        gate = state["gates"].setdefault(gate_id, {})
        gate.update(
            {
                "status": "pending",
                "kind": "",
                "decision_ref": "",
                "confirmed_at": "",
                "evidence": {"source": "", "ref": "", "summary": ""},
            }
        )
    timestamp = now_iso()
    state.setdefault("invalidations", []).append(
        {
            "from_gate": args.from_gate,
            "reason": args.reason,
            "artifact": args.artifact,
            "invalidated_at": timestamp,
        }
    )
    state["current_phase"] = phase_for(state)
    state["updated_at"] = timestamp
    atomic_write(path, state)
    print(f"invalidated from {args.from_gate}; current phase: {state['current_phase']}")
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    status = subparsers.add_parser("status")
    status.add_argument("planning_dir", type=Path)
    status.add_argument("--json", action="store_true")

    confirm = subparsers.add_parser("confirm")
    confirm.add_argument("planning_dir", type=Path)
    confirm.add_argument("--gate", required=True, choices=GATE_ORDER)
    confirm.add_argument("--decision-ref", required=True)
    confirm.add_argument("--evidence-ref", required=True, help="Reference to the actual user message or review event")
    confirm.add_argument("--summary", required=True)
    confirm.add_argument("--confirmed-at")

    invalidate = subparsers.add_parser("invalidate")
    invalidate.add_argument("planning_dir", type=Path)
    invalidate.add_argument("--from-gate", required=True, choices=GATE_ORDER)
    invalidate.add_argument("--reason", required=True)
    invalidate.add_argument("--artifact", required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = args.planning_dir.expanduser().resolve()
    if args.command == "status":
        return command_status(root, args.json)
    if args.command == "confirm":
        return command_confirm(args)
    return command_invalidate(args)


if __name__ == "__main__":
    raise SystemExit(main())
