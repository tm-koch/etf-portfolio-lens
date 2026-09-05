import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
WEB_ROOT = REPOSITORY_ROOT / "web"
CACHE_HELPER = REPOSITORY_ROOT / "scripts" / "pwa-cache-generation.ps1"


class PwaCacheGenerationTests(unittest.TestCase):
    def run_generation(self, root: Path) -> str:
        command = f". '{CACHE_HELPER}'; " f"Get-PwaCacheGeneration -Root '{root}'"
        result = subprocess.run(
            ["pwsh", "-NoProfile", "-Command", command],
            cwd=REPOSITORY_ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        return result.stdout.strip()

    def test_generation_is_deterministic_and_changes_with_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            first_root = Path(temporary_directory) / "first"
            second_root = Path(temporary_directory) / "second"
            shutil.copytree(WEB_ROOT, first_root)
            shutil.copytree(WEB_ROOT, second_root)

            first_generation = self.run_generation(first_root)
            self.assertEqual(first_generation, self.run_generation(first_root))

            manifest = json.loads(
                (second_root / "manifest.json").read_text(encoding="utf-8")
            )
            manifest["name"] = "Changed ETF Portfolio Lens"
            (second_root / "manifest.json").write_text(
                json.dumps(manifest), encoding="utf-8"
            )

            self.assertNotEqual(first_generation, self.run_generation(second_root))

    def test_published_worker_replacement_does_not_modify_source_worker(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            published_worker = Path(temporary_directory) / "sw.js"
            shutil.copy2(WEB_ROOT / "sw.js", published_worker)
            command = (
                f". '{CACHE_HELPER}'; "
                f"Set-PwaServiceWorkerGeneration -ServiceWorkerPath '{published_worker}' -Generation '0123456789abcdef'; "
                f"Get-PwaServiceWorkerGeneration -ServiceWorkerContent (Get-Content -Raw '{published_worker}')"
            )
            result = subprocess.run(
                ["pwsh", "-NoProfile", "-Command", command],
                cwd=REPOSITORY_ROOT,
                check=True,
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.stdout.strip(), "0123456789abcdef")
            self.assertIn(
                "__PWA_CACHE_GENERATION__",
                (WEB_ROOT / "sw.js").read_text(encoding="utf-8"),
            )

    def test_generation_rejects_missing_cache_sensitive_asset(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory) / "web"
            shutil.copytree(WEB_ROOT, root)
            (root / "manifest.json").unlink()
            command = f". '{CACHE_HELPER}'; " f"Get-PwaCacheGeneration -Root '{root}'"
            result = subprocess.run(
                ["pwsh", "-NoProfile", "-Command", command],
                cwd=REPOSITORY_ROOT,
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Cache-sensitive PWA asset is missing", result.stderr)

    def test_worker_replacement_rejects_missing_generation_token(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            worker = Path(temporary_directory) / "sw.js"
            worker.write_text("const CACHE_VERSION = 'old';", encoding="utf-8")
            command = (
                f". '{CACHE_HELPER}'; "
                f"Set-PwaServiceWorkerGeneration -ServiceWorkerPath '{worker}' -Generation '0123456789abcdef'"
            )
            result = subprocess.run(
                ["pwsh", "-NoProfile", "-Command", command],
                cwd=REPOSITORY_ROOT,
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn(
                "does not contain the __PWA_CACHE_GENERATION__ token", result.stderr
            )


if __name__ == "__main__":
    unittest.main()
