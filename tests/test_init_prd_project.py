from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "init_prd_project.py"


class InitPrdProjectTest(unittest.TestCase):
    def test_standard_scaffold_includes_named_service_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            subprocess.run(["python3", str(SCRIPT), "서비스 계약", "--root", temp], check=True, capture_output=True, text=True)
            manifest_path = Path(temp) / "서비스-계약" / "02.6-service-manifest.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            self.assertEqual(manifest["project"]["name"], "서비스 계약")
            self.assertEqual(manifest["project"]["mode"], "standard")
            self.assertEqual(manifest["evidence"]["demo_file"], "prototypes/서비스-계약-demo.html")
            dashboard = (manifest_path.parent / "00-review-dashboard.html").read_text(encoding="utf-8")
            product_definition = json.loads((manifest_path.parent / "02.1-product-definition.json").read_text(encoding="utf-8"))
            planning_review = json.loads((manifest_path.parent / "02.05-planning-quality-review.json").read_text(encoding="utf-8"))
            self.assertIn('data-readiness-status="not-evaluated"', dashboard)
            self.assertEqual(product_definition["status"], "draft")
            self.assertEqual(planning_review["status"], "draft")
            self.assertEqual(planning_review["profile"], "standard")
            self.assertEqual(len(planning_review["lenses"]), 6)
            self.assertTrue((manifest_path.parent / "03-design-brief.md").exists())
            self.assertTrue((manifest_path.parent / "04.2-backend-systems-brief.md").exists())
            self.assertFalse((manifest_path.parent / "05-design-acceptance.json").exists())
            self.assertFalse((manifest_path.parent / "04.36-clickable-demo.md").exists())
            self.assertFalse((manifest_path.parent / "prototypes").exists())

    def test_lite_scaffold_keeps_manifest_but_marks_lite(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            subprocess.run(["python3", str(SCRIPT), "Lite Product", "--root", temp, "--lite"], check=True, capture_output=True, text=True)
            target = Path(temp) / "lite-product"
            manifest = json.loads((target / "02.6-service-manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest["project"]["mode"], "lite")
            self.assertTrue((target / "02.1-product-definition.json").exists())
            planning_review = json.loads((target / "02.05-planning-quality-review.json").read_text(encoding="utf-8"))
            self.assertEqual(planning_review["profile"], "lite")
            self.assertTrue((target / "01.6-parallel-concepts.md").exists())
            self.assertTrue((target / "01.8-positioning-brand.md").exists())
            self.assertTrue((target / "02-mechanisms.md").exists())
            self.assertTrue((target / "03-design-brief.md").exists())
            self.assertFalse((target / "05-design-acceptance.json").exists())
            self.assertFalse((target / "04.36-clickable-demo.md").exists())

    def test_deep_scaffold_uses_deep_profiles_but_still_stops_at_planning(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            subprocess.run(["python3", str(SCRIPT), "Deep Product", "--root", temp, "--deep"], check=True, capture_output=True, text=True)
            target = Path(temp) / "deep-product"
            manifest = json.loads((target / "02.6-service-manifest.json").read_text(encoding="utf-8"))
            planning_review = json.loads((target / "02.05-planning-quality-review.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest["project"]["mode"], "deep")
            self.assertEqual(planning_review["profile"], "deep")
            self.assertTrue((target / "03-design-brief.md").exists())
            self.assertTrue((target / "04.55-risk-register.md").exists())
            self.assertFalse((target / "05-design-acceptance.json").exists())
            self.assertFalse((target / "04.36-clickable-demo.md").exists())

    def test_with_design_adds_optional_visual_and_prototype_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            subprocess.run(
                ["python3", str(SCRIPT), "Designed Product", "--root", temp, "--with-design"],
                check=True,
                capture_output=True,
                text=True,
            )
            target = Path(temp) / "designed-product"
            design_acceptance = json.loads((target / "05-design-acceptance.json").read_text(encoding="utf-8"))
            self.assertEqual(design_acceptance["status"], "pending")
            self.assertTrue((target / "03-design-brief.md").exists())
            self.assertTrue((target / "03.4-visual-directions.md").exists())
            self.assertTrue((target / "03.5-art-direction-brief.md").exists())
            self.assertTrue((target / "04.36-clickable-demo.md").exists())
            self.assertTrue((target / "05-engineering-handoff.md").exists())
            self.assertTrue((target / "prototypes").is_dir())

    def test_with_design_does_not_overwrite_existing_planning_files(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            subprocess.run(["python3", str(SCRIPT), "Resume", "--root", temp], check=True, capture_output=True, text=True)
            brief = Path(temp) / "resume" / "00-brief.md"
            brief.write_text("# My existing brief\n", encoding="utf-8")
            subprocess.run(
                ["python3", str(SCRIPT), "Resume", "--root", temp, "--with-design"],
                check=True,
                capture_output=True,
                text=True,
            )
            self.assertEqual(brief.read_text(encoding="utf-8"), "# My existing brief\n")
            self.assertTrue((brief.parent / "05-design-acceptance.json").exists())


if __name__ == "__main__":
    unittest.main()
