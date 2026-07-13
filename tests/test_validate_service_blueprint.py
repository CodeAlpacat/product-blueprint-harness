from __future__ import annotations

import copy
import importlib.util
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests" / "fixtures" / "valid-standard"
SPEC = importlib.util.spec_from_file_location("validate_service_blueprint", ROOT / "scripts" / "validate_service_blueprint.py")
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class ServiceBlueprintValidatorTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name) / "plan"
        shutil.copytree(FIXTURE, self.root)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def validate(self, profile: str | None = None):
        return MODULE.Validator(self.root, profile).run()

    def manifest(self) -> dict:
        return json.loads((self.root / "02.6-service-manifest.json").read_text(encoding="utf-8"))

    def write_manifest(self, manifest: dict) -> None:
        (self.root / "02.6-service-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    @staticmethod
    def codes(report: dict) -> set[str]:
        return {finding["code"] for finding in report["findings"]}

    def test_ac10_valid_standard_passes(self) -> None:
        report = self.validate()
        self.assertEqual(report["status"], "pass")
        self.assertTrue(report["engineering_ready"])
        self.assertFalse(report["user_validated"])
        self.assertEqual(report["findings"], [])

    def test_ac01_missing_required_artifact_fails(self) -> None:
        (self.root / "04.36-clickable-demo.md").unlink()
        report = self.validate()
        self.assertIn("REQUIRED_ARTIFACT_MISSING", self.codes(report))

    def test_ac02_false_readiness_claim_fails(self) -> None:
        manifest = self.manifest()
        manifest["surfaces"][0]["purpose"] = ""
        self.write_manifest(manifest)
        report = self.validate()
        self.assertIn("READINESS_CLAIM_CONFLICT", self.codes(report))

    def test_ac03_uncontracted_control_fails(self) -> None:
        demo = self.root / "prototypes" / "fixture-demo.html"
        demo.write_text(demo.read_text().replace("</body>", '<button id="dead">Dead</button></body>'), encoding="utf-8")
        report = self.validate()
        self.assertIn("UNCONTRACTED_CONTROL", self.codes(report))

    def test_ac04_unreachable_surface_fails(self) -> None:
        manifest = self.manifest()
        extra = copy.deepcopy(manifest["surfaces"][1])
        extra.update({"id": "settings", "label": "Settings", "purpose": "Change settings.", "entry_action_ids": [], "exit_action_ids": []})
        extra["prototype"]["element_id"] = "surface-settings"
        manifest["surfaces"].append(extra)
        self.write_manifest(manifest)
        demo = self.root / "prototypes" / "fixture-demo.html"
        demo.write_text(demo.read_text().replace("</body>", '<section id="surface-settings" data-surface="settings"></section></body>'), encoding="utf-8")
        report = self.validate()
        self.assertIn("UNREACHABLE_SURFACE", self.codes(report))

    def test_ac05_incomplete_operation_fails(self) -> None:
        manifest = self.manifest()
        manifest["operations"][0]["recovery"] = ""
        self.write_manifest(manifest)
        report = self.validate()
        self.assertIn("INCOMPLETE_OPERATION_CONTRACT", self.codes(report))

    def test_ac06_state_without_dom_evidence_fails(self) -> None:
        manifest = self.manifest()
        manifest["states"][0]["prototype"]["element_id"] = "missing-loading-state"
        self.write_manifest(manifest)
        report = self.validate()
        self.assertIn("STATE_NOT_REPRODUCIBLE", self.codes(report))

    def test_ac07_deferred_entry_without_current_behavior_fails(self) -> None:
        manifest = self.manifest()
        manifest["release_profile"]["excluded"] = [{"id": "notifications", "decision_ref": "DEC-7", "current_entry_behavior": ""}]
        self.write_manifest(manifest)
        report = self.validate()
        self.assertIn("DEFERRED_ENTRY_UNDEFINED", self.codes(report))

    def test_ac08_missing_resume_lifecycle_fails(self) -> None:
        manifest = self.manifest()
        manifest["journeys"][0]["refresh_resume"] = ""
        self.write_manifest(manifest)
        report = self.validate()
        self.assertIn("JOURNEY_LIFECYCLE_MISSING", self.codes(report))

    def test_ac09_missing_responsive_rule_fails(self) -> None:
        manifest = self.manifest()
        manifest["surfaces"][0]["responsive"]["derivation_rule"] = ""
        self.write_manifest(manifest)
        report = self.validate()
        self.assertIn("RESPONSIVE_EVIDENCE_MISSING", self.codes(report))

    def test_ac11_heuristic_does_not_claim_user_validation(self) -> None:
        report = self.validate()
        self.assertEqual(report["status"], "pass")
        self.assertFalse(report["user_validated"])

    def test_ac12_lite_can_pass_but_is_not_engineering_ready(self) -> None:
        manifest = self.manifest()
        manifest["project"]["mode"] = "lite"
        self.write_manifest(manifest)
        for relative in MODULE.STANDARD_ARTIFACTS:
            if relative not in MODULE.LITE_ARTIFACTS:
                path = self.root / relative
                if path.exists():
                    path.unlink()
        report = self.validate()
        self.assertEqual(report["status"], "lite-pass")
        self.assertFalse(report["engineering_ready"])

    def test_transition_dom_must_match_manifest_target(self) -> None:
        demo = self.root / "prototypes" / "fixture-demo.html"
        demo.write_text(demo.read_text().replace('data-go="detail"', 'data-go="home"'), encoding="utf-8")
        report = self.validate()
        self.assertIn("TRANSITION_DOM_MISMATCH", self.codes(report))

    def test_surface_maturity_cannot_self_pass_with_verified_false(self) -> None:
        manifest = self.manifest()
        manifest["surfaces"][0]["status"]["verified"] = False
        self.write_manifest(manifest)
        report = self.validate()
        self.assertIn("SURFACE_NOT_VERIFIED", self.codes(report))

    def test_wiring_matrix_must_match_action_source_and_target(self) -> None:
        manifest = self.manifest()
        manifest["surfaces"][1]["entry_action_ids"] = []
        self.write_manifest(manifest)
        report = self.validate()
        self.assertIn("WIRING_MATRIX_MISMATCH", self.codes(report))

    def test_ai_assist_requires_five_cell_review_loop(self) -> None:
        manifest = self.manifest()
        manifest["ai_assists"] = [{"id": "draft-summary", "trigger_action_id": "retry-detail", "input": "Item", "result_widget": "Preview", "editable_unit": "Paragraph", "save_destination": ""}]
        self.write_manifest(manifest)
        report = self.validate()
        self.assertIn("AI_ASSIST_HANDWAVE", self.codes(report))

    def test_effect_dom_must_match_manifest_effect(self) -> None:
        demo = self.root / "prototypes" / "fixture-demo.html"
        demo.write_text(demo.read_text().replace('data-effect="replace-error-with-detail"', 'data-effect="wrong"'), encoding="utf-8")
        report = self.validate()
        self.assertIn("EFFECT_DOM_MISMATCH", self.codes(report))

    def test_operation_decision_needed_blocks_readiness(self) -> None:
        manifest = self.manifest()
        manifest["operations"][0]["consistency"] = "decision-needed:DEC-9"
        self.write_manifest(manifest)
        report = self.validate()
        self.assertIn("OPERATION_DECISION_BLOCKER", self.codes(report))

    def test_accepted_limitation_requires_decision_owner_and_consequence(self) -> None:
        manifest = self.manifest()
        manifest["release_profile"]["accepted_limitations"] = [{"id": "slow-search", "decision_ref": "DEC-11"}]
        self.write_manifest(manifest)
        report = self.validate()
        self.assertIn("ACCEPTED_LIMITATION_INCOMPLETE", self.codes(report))

    def test_report_files_are_generated(self) -> None:
        report = self.validate()
        MODULE.write_report(self.root, report)
        written = json.loads((self.root / "05-readiness-report.json").read_text(encoding="utf-8"))
        self.assertEqual(written["manifest_sha256"], report["manifest_sha256"])
        self.assertIn("Status: **pass**", (self.root / "05-readiness-report.md").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
