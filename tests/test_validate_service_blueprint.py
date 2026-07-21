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

    def validate(self, profile: str | None = None, stage: str = "handoff"):
        return MODULE.Validator(self.root, profile, stage).run()

    def manifest(self) -> dict:
        return json.loads((self.root / "02.6-service-manifest.json").read_text(encoding="utf-8"))

    def write_manifest(self, manifest: dict) -> None:
        (self.root / "02.6-service-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    def planning_review(self) -> dict:
        return json.loads((self.root / "02.05-planning-quality-review.json").read_text(encoding="utf-8"))

    def write_planning_review(self, review: dict) -> None:
        (self.root / "02.05-planning-quality-review.json").write_text(json.dumps(review, indent=2) + "\n", encoding="utf-8")

    def product_definition(self) -> dict:
        return json.loads((self.root / "02.1-product-definition.json").read_text(encoding="utf-8"))

    def write_product_definition(self, definition: dict) -> None:
        (self.root / "02.1-product-definition.json").write_text(json.dumps(definition, indent=2) + "\n", encoding="utf-8")

    def design_acceptance(self) -> dict:
        return json.loads((self.root / "05-design-acceptance.json").read_text(encoding="utf-8"))

    def write_design_acceptance(self, acceptance: dict) -> None:
        (self.root / "05-design-acceptance.json").write_text(json.dumps(acceptance, indent=2) + "\n", encoding="utf-8")

    @staticmethod
    def codes(report: dict) -> set[str]:
        return {finding["code"] for finding in report["findings"]}

    def test_ac10_valid_standard_passes(self) -> None:
        report = self.validate()
        self.assertEqual(report["status"], "handoff-pass")
        self.assertFalse(report["engineering_ready"])
        self.assertTrue(report["design_accepted"])
        self.assertTrue(report["product_handoff_ready"])
        self.assertFalse(report["user_validated"])
        self.assertEqual(report["findings"], [])

    def test_ac01_missing_required_artifact_fails(self) -> None:
        (self.root / "04.36-clickable-demo.md").unlink()
        report = self.validate()
        self.assertIn("REQUIRED_ARTIFACT_MISSING", self.codes(report))

    def test_contract_requires_concept_brand_and_mechanism_artifacts(self) -> None:
        (self.root / "01.8-positioning-brand.md").unlink()
        report = self.validate(stage="contract")
        self.assertIn("REQUIRED_ARTIFACT_MISSING", self.codes(report))

    def test_planning_review_requires_all_six_lenses(self) -> None:
        review = self.planning_review()
        review["lenses"] = [lens for lens in review["lenses"] if lens["id"] != "brand"]
        self.write_planning_review(review)
        report = self.validate(stage="contract")
        self.assertIn("PLANNING_LENS_MISSING", self.codes(report))

    def test_open_p0_or_p1_planning_finding_blocks_contract(self) -> None:
        review = self.planning_review()
        review["findings"][0]["status"] = "open"
        self.write_planning_review(review)
        report = self.validate(stage="contract")
        self.assertIn("PLANNING_BLOCKER_OPEN", self.codes(report))

    def test_planning_review_requires_explicit_mvp_lock(self) -> None:
        review = self.planning_review()
        review["status"] = "draft"
        review["mvp_lock"]["status"] = "pending"
        self.write_planning_review(review)
        report = self.validate(stage="contract")
        self.assertIn("PLANNING_REVIEW_UNCONFIRMED", self.codes(report))
        self.assertIn("MVP_LOCK_UNCONFIRMED", self.codes(report))

    def test_mvp_lock_decision_ref_must_exist_in_decision_log(self) -> None:
        review = self.planning_review()
        review["mvp_lock"]["decision_ref"] = "DEC-MISSING"
        self.write_planning_review(review)
        report = self.validate(stage="contract")
        self.assertIn("MVP_LOCK_DECISION_REF_MISSING", self.codes(report))

    def test_planning_review_rejects_stale_prd(self) -> None:
        prd = self.root / "02-prd.md"
        prd.write_text(prd.read_text(encoding="utf-8") + "\nChanged after review.\n", encoding="utf-8")
        report = self.validate(stage="contract")
        self.assertIn("PLANNING_REVIEW_STALE", self.codes(report))

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
        self.assertEqual(report["status"], "handoff-pass")
        self.assertFalse(report["user_validated"])

    def test_ac12_lite_can_pass_but_is_not_engineering_ready(self) -> None:
        manifest = self.manifest()
        manifest["project"]["mode"] = "lite"
        self.write_manifest(manifest)
        planning_review = self.planning_review()
        planning_review["profile"] = "lite"
        self.write_planning_review(planning_review)
        for relative in MODULE.STANDARD_ARTIFACTS:
            if relative not in MODULE.LITE_ARTIFACTS:
                path = self.root / relative
                if path.exists():
                    path.unlink()
        report = self.validate()
        self.assertEqual(report["status"], "lite-pass")
        self.assertFalse(report["engineering_ready"])

    def test_lite_manifest_cannot_be_an_empty_scaffold(self) -> None:
        manifest = self.manifest()
        manifest["project"]["mode"] = "lite"
        manifest["surfaces"] = []
        manifest["actions"] = []
        manifest["journeys"] = []
        self.write_manifest(manifest)
        report = self.validate(stage="contract")
        self.assertIn("CONTRACT_COLLECTION_EMPTY", self.codes(report))

    def test_unconfirmed_product_definition_blocks_contract(self) -> None:
        definition = self.product_definition()
        definition["status"] = "draft"
        self.write_product_definition(definition)
        report = self.validate(stage="contract")
        self.assertIn("PRODUCT_DEFINITION_UNCONFIRMED", self.codes(report))

    def test_p0_requirement_without_required_mapping_blocks_contract(self) -> None:
        definition = self.product_definition()
        definition["requirements"].append({
            "id": "save-favorite",
            "statement": "A guest can save a favorite.",
            "kind": "interaction",
            "priority": "P0",
            "status": "included",
            "persona_ids": ["guest"],
            "source_refs": ["02-prd.md#favorite"],
            "decision_ref": "DEC-2",
            "acceptance_outcomes": ["The favorite is visible after refresh."],
        })
        self.write_product_definition(definition)
        report = self.validate(stage="contract")
        self.assertIn("P0_REQUIREMENT_UNCOVERED", self.codes(report))

    def test_entry_point_without_journey_blocks_contract(self) -> None:
        definition = self.product_definition()
        definition["entry_points"].append({
            "id": "shared-link",
            "label": "Shared link",
            "persona_id": "guest",
            "trigger": "Open a shared item URL",
            "context": "The item may no longer exist",
            "expected_outcome": "See the item or a recoverable not-found state",
            "lifecycle": ["external-result", "refresh", "back"],
            "source_refs": ["02-prd.md#shared-link"],
        })
        self.write_product_definition(definition)
        report = self.validate(stage="contract")
        self.assertIn("ENTRY_POINT_UNCOVERED", self.codes(report))

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

    def test_declared_risk_domain_requires_risk_register(self) -> None:
        manifest = self.manifest()
        manifest["release_profile"]["risk_domains"] = ["payments"]
        self.write_manifest(manifest)
        report = self.validate()
        self.assertIn("RISK_REGISTER_MISSING", self.codes(report))

    def test_evidence_cannot_escape_planning_directory(self) -> None:
        manifest = self.manifest()
        manifest["surfaces"][0]["prototype"]["file"] = "../outside.html"
        self.write_manifest(manifest)
        report = self.validate()
        self.assertIn("EVIDENCE_PATH_OUTSIDE_PROJECT", self.codes(report))

    def test_not_ready_phrase_is_not_a_positive_readiness_claim(self) -> None:
        dashboard = self.root / "00-review-dashboard.html"
        dashboard.write_text("<html><body>Not ready for engineering</body></html>", encoding="utf-8")
        handoff = self.root / "05-engineering-handoff.md"
        handoff.write_text(handoff.read_text(encoding="utf-8").replace("planning-readiness: pass", "planning-readiness: pending"), encoding="utf-8")
        manifest = self.manifest()
        manifest["surfaces"][0]["purpose"] = ""
        self.write_manifest(manifest)
        report = self.validate()
        conflicts = [item for item in report["findings"] if item["code"] == "READINESS_CLAIM_CONFLICT"]
        self.assertEqual(conflicts, [])

    def test_report_files_are_generated(self) -> None:
        report = self.validate()
        MODULE.write_report(self.root, report)
        written = json.loads((self.root / "05-readiness-report.json").read_text(encoding="utf-8"))
        self.assertEqual(written["manifest_sha256"], report["manifest_sha256"])
        self.assertIn("Status: **handoff-pass**", (self.root / "05-readiness-report.md").read_text(encoding="utf-8"))

    def test_runtime_report_must_match_current_manifest_and_demo_hashes(self) -> None:
        runtime = self.root / "04.37-runtime-verification.json"
        report = json.loads(runtime.read_text(encoding="utf-8"))
        report["demo_sha256"] = "stale"
        runtime.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        result = self.validate(stage="prototype")
        self.assertIn("RUNTIME_REPORT_STALE", self.codes(result))

    def test_runtime_report_must_cover_every_effect(self) -> None:
        runtime = self.root / "04.37-runtime-verification.json"
        report = json.loads(runtime.read_text(encoding="utf-8"))
        report["effects"] = []
        runtime.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        result = self.validate(stage="prototype")
        self.assertIn("RUNTIME_EFFECT_UNVERIFIED", self.codes(result))

    def test_contract_stage_passes_before_prototype_exists(self) -> None:
        manifest = self.manifest()
        for surface in manifest["surfaces"]:
            surface["status"] = {"defined": True, "prototyped": False, "wired": False, "contracted": False, "verified": False}
        self.write_manifest(manifest)
        shutil.rmtree(self.root / "prototypes")
        report = self.validate(stage="contract")
        self.assertEqual(report["status"], "contract-pass")
        self.assertFalse(report["engineering_ready"])

    def test_planning_stage_passes_without_visual_design_artifacts(self) -> None:
        for relative in MODULE.DESIGN_ARTIFACTS:
            if relative not in MODULE.PLANNING_ARTIFACTS:
                path = self.root / relative
                if path.is_file():
                    path.unlink()
        report = self.validate(stage="planning")
        self.assertEqual(report["status"], "planning-pass")
        self.assertTrue(report["planning_ready"])
        self.assertFalse(report["prototype_ready"])
        self.assertFalse(report["design_accepted"])

    def test_planning_stage_requires_design_brief(self) -> None:
        (self.root / "03-design-brief.md").unlink()
        report = self.validate(stage="planning")
        self.assertIn("REQUIRED_ARTIFACT_MISSING", self.codes(report))

    def test_design_stage_rejects_design_brief_changed_after_approval(self) -> None:
        brief = self.root / "03-design-brief.md"
        brief.write_text(brief.read_text(encoding="utf-8") + "\nChanged after approval.\n", encoding="utf-8")
        report = self.validate(stage="design")
        self.assertIn("DESIGN_BASELINE_STALE", self.codes(report))

    def test_prototype_stage_does_not_require_handoff_yet(self) -> None:
        (self.root / "04.4-prototype-test.md").unlink()
        (self.root / "05-engineering-handoff.md").unlink()
        report = self.validate(stage="prototype")
        self.assertEqual(report["status"], "prototype-pass")
        self.assertFalse(report["engineering_ready"])

    def test_prototype_stage_does_not_require_design_acceptance_yet(self) -> None:
        (self.root / "05-design-acceptance.json").unlink()
        report = self.validate(stage="prototype")
        self.assertEqual(report["status"], "prototype-pass")
        self.assertTrue(report["prototype_ready"])

    def test_design_stage_requires_explicit_approval(self) -> None:
        acceptance = self.design_acceptance()
        acceptance["status"] = "pending"
        self.write_design_acceptance(acceptance)
        report = self.validate(stage="design")
        self.assertIn("DESIGN_NOT_APPROVED", self.codes(report))
        self.assertFalse(report["design_accepted"])

    def test_design_stage_requires_compared_visual_directions(self) -> None:
        (self.root / "03.4-visual-directions.md").unlink()
        report = self.validate(stage="design")
        self.assertIn("REQUIRED_ARTIFACT_MISSING", self.codes(report))

    def test_design_stage_requires_implementation_fidelity_react_sources(self) -> None:
        acceptance = self.design_acceptance()
        acceptance.pop("visual_implementation")
        self.write_design_acceptance(acceptance)
        report = self.validate(stage="design")
        self.assertIn("IMPLEMENTATION_FIDELITY_MISSING", self.codes(report))

    def test_design_stage_rejects_stale_react_source(self) -> None:
        source = self.root / "visual-workbench" / "boards" / "DepthBoard.tsx"
        source.write_text(source.read_text(encoding="utf-8") + "\n", encoding="utf-8")
        report = self.validate(stage="design")
        self.assertIn("IMPLEMENTATION_SOURCE_STALE", self.codes(report))

    def test_design_stage_requires_visual_evidence_source_trace(self) -> None:
        acceptance = self.design_acceptance()
        acceptance["visual_evidence"][0].pop("render_source_ref")
        self.write_design_acceptance(acceptance)
        report = self.validate(stage="design")
        self.assertIn("VISUAL_SOURCE_TRACE_MISSING", self.codes(report))

    def test_design_stage_rejects_stale_bound_source(self) -> None:
        prd = self.root / "02-prd.md"
        prd.write_text(prd.read_text(encoding="utf-8") + "\nchanged\n", encoding="utf-8")
        report = self.validate(stage="design")
        self.assertIn("DESIGN_BASELINE_STALE", self.codes(report))

    def test_design_stage_requires_every_p0_viewport(self) -> None:
        acceptance = self.design_acceptance()
        acceptance["visual_evidence"] = [row for row in acceptance["visual_evidence"] if row["id"] != "detail-desktop"]
        acceptance["review_rounds"][1]["reviewed_evidence_ids"].remove("detail-desktop")
        self.write_design_acceptance(acceptance)
        report = self.validate(stage="design")
        self.assertIn("VISUAL_VIEWPORT_COVERAGE_MISSING", self.codes(report))

    def test_design_stage_requires_states_at_each_viewport(self) -> None:
        acceptance = self.design_acceptance()
        next(row for row in acceptance["visual_evidence"] if row["id"] == "detail-desktop")["state_ids"] = []
        self.write_design_acceptance(acceptance)
        report = self.validate(stage="design")
        self.assertIn("VISUAL_STATE_COVERAGE_MISSING", self.codes(report))

    def test_design_stage_rejects_stale_visual_evidence(self) -> None:
        visual = self.root / "screenshots" / "visual-home-mobile.svg"
        visual.write_text(visual.read_text(encoding="utf-8") + "\n", encoding="utf-8")
        report = self.validate(stage="design")
        self.assertIn("VISUAL_EVIDENCE_STALE", self.codes(report))

    def test_design_stage_rejects_planning_review_changed_after_approval(self) -> None:
        review = self.planning_review()
        review["reviewed_at"] = "2026-07-21T00:00:00Z"
        self.write_planning_review(review)
        report = self.validate(stage="design")
        self.assertIn("DESIGN_BASELINE_STALE", self.codes(report))

    def test_unresolved_p0_design_finding_blocks_acceptance(self) -> None:
        acceptance = self.design_acceptance()
        acceptance["findings"][0]["status"] = "deferred"
        self.write_design_acceptance(acceptance)
        report = self.validate(stage="design")
        self.assertIn("UNRESOLVED_P0_DESIGN_FINDING", self.codes(report))

    def test_owner_approval_does_not_claim_target_user_validation(self) -> None:
        report = self.validate(stage="design")
        self.assertTrue(report["design_owner_approved"])
        self.assertTrue(report["design_accepted"])
        self.assertFalse(report["user_validated"])

    def test_design_stage_requires_developer_lens_coverage(self) -> None:
        acceptance = self.design_acceptance()
        acceptance["feasibility_checks"] = [row for row in acceptance["feasibility_checks"] if row["id"] != "load-detail-backend"]
        acceptance["approval"]["feasibility_check_ids"].remove("load-detail-backend")
        self.write_design_acceptance(acceptance)
        report = self.validate(stage="design")
        self.assertIn("FEASIBILITY_COVERAGE_MISSING", self.codes(report))

    def test_infeasible_behavior_blocks_design_acceptance(self) -> None:
        acceptance = self.design_acceptance()
        acceptance["feasibility_checks"][0]["verdict"] = "infeasible"
        self.write_design_acceptance(acceptance)
        report = self.validate(stage="design")
        self.assertIn("FEASIBILITY_BLOCKER_OPEN", self.codes(report))

    def test_constraint_requires_absorbed_design_evidence(self) -> None:
        acceptance = self.design_acceptance()
        check = next(row for row in acceptance["feasibility_checks"] if row["id"] == "detail-frontend")
        check["design_resolution"] = ""
        check["resolution_evidence_refs"] = []
        self.write_design_acceptance(acceptance)
        report = self.validate(stage="design")
        self.assertIn("FEASIBILITY_CONSTRAINT_UNABSORBED", self.codes(report))

    def test_constraint_rejects_unknown_design_evidence(self) -> None:
        acceptance = self.design_acceptance()
        check = next(row for row in acceptance["feasibility_checks"] if row["id"] == "detail-frontend")
        check["resolution_evidence_refs"] = ["missing-visual"]
        self.write_design_acceptance(acceptance)
        report = self.validate(stage="design")
        self.assertIn("FEASIBILITY_CONSTRAINT_UNABSORBED", self.codes(report))

    def test_constraint_rejects_unrelated_design_evidence(self) -> None:
        acceptance = self.design_acceptance()
        check = next(row for row in acceptance["feasibility_checks"] if row["id"] == "detail-frontend")
        check["resolution_evidence_refs"] = ["home-mobile"]
        self.write_design_acceptance(acceptance)
        report = self.validate(stage="design")
        self.assertIn("FEASIBILITY_CONSTRAINT_UNABSORBED", self.codes(report))

    def test_changed_feasibility_review_requires_user_reapproval(self) -> None:
        acceptance = self.design_acceptance()
        acceptance["approval"]["feasibility_check_ids"].remove("detail-frontend")
        self.write_design_acceptance(acceptance)
        report = self.validate(stage="design")
        self.assertIn("FEASIBILITY_REAPPROVAL_REQUIRED", self.codes(report))

    def test_changed_feasibility_verdict_with_same_id_requires_user_reapproval(self) -> None:
        acceptance = self.design_acceptance()
        check = next(row for row in acceptance["feasibility_checks"] if row["id"] == "home-frontend")
        check["evidence"] = "04.5-feasibility-review.md#revised-consultation"
        self.write_design_acceptance(acceptance)
        report = self.validate(stage="design")
        self.assertIn("FEASIBILITY_REAPPROVAL_REQUIRED", self.codes(report))

    def test_handoff_stops_at_accepted_design_boundary(self) -> None:
        report = self.validate(stage="handoff")
        self.assertEqual(report["status"], "handoff-pass")
        self.assertTrue(report["design_handoff_ready"])
        self.assertTrue(report["ready_for_technical_design"])
        self.assertFalse(report["technical_design_ready"])
        self.assertFalse(report["implementation_ready"])
        self.assertFalse(report["engineering_ready"])


if __name__ == "__main__":
    unittest.main()
