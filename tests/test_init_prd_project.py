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

    def test_lite_scaffold_keeps_manifest_but_marks_lite(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            subprocess.run(["python3", str(SCRIPT), "Lite Product", "--root", temp, "--lite"], check=True, capture_output=True, text=True)
            target = Path(temp) / "lite-product"
            manifest = json.loads((target / "02.6-service-manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest["project"]["mode"], "lite")
            self.assertFalse((target / "04.36-clickable-demo.md").exists())


if __name__ == "__main__":
    unittest.main()
