from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INIT = ROOT / "scripts" / "init_prd_project.py"
STATE = ROOT / "scripts" / "workflow_state.py"


class WorkflowStateTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        subprocess.run(["python3", str(INIT), "State Fixture", "--root", self.temp.name], check=True, capture_output=True, text=True)
        self.plan = Path(self.temp.name) / "state-fixture"

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_confirm_records_explicit_user_evidence_and_routes_next_gate(self) -> None:
        subprocess.run(
            [
                "python3",
                str(STATE),
                "confirm",
                str(self.plan),
                "--gate",
                "product-direction",
                "--decision-ref",
                "DEC-1",
                "--evidence-ref",
                "conversation:message-42",
                "--summary",
                "The user selected concept A.",
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        state = json.loads((self.plan / "00-workflow-state.json").read_text(encoding="utf-8"))
        self.assertEqual(state["gates"]["product-direction"]["kind"], "explicit-user")
        self.assertEqual(state["history"][-1]["actor"], "user")
        result = subprocess.run(
            ["python3", str(STATE), "status", str(self.plan), "--json"],
            check=True,
            capture_output=True,
            text=True,
        )
        status = json.loads(result.stdout)
        self.assertEqual(status["next_gate"], "brand-direction")
        self.assertEqual(status["next_skill"], "product-blueprint:positioning-brand")

    def test_invalidate_clears_changed_gate_and_every_downstream_gate(self) -> None:
        state_path = self.plan / "00-workflow-state.json"
        state = json.loads(state_path.read_text(encoding="utf-8"))
        for gate_id in state["gates"]:
            state["gates"][gate_id].update({"status": "confirmed", "kind": "explicit-user", "decision_ref": "DEC-X"})
        state_path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
        subprocess.run(
            [
                "python3",
                str(STATE),
                "invalidate",
                str(self.plan),
                "--from-gate",
                "first-version-scope",
                "--reason",
                "The audience changed.",
                "--artifact",
                "00-brief.md",
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        updated = json.loads(state_path.read_text(encoding="utf-8"))
        self.assertEqual(updated["gates"]["brand-direction"]["status"], "confirmed")
        self.assertEqual(updated["gates"]["first-version-scope"]["status"], "pending")
        self.assertEqual(updated["gates"]["key-screen"]["status"], "pending")
        self.assertEqual(updated["current_phase"], "planning-review")


if __name__ == "__main__":
    unittest.main()
