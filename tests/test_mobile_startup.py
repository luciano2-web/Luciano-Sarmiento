"""Regression tests: console startup must work without optional GUI/model packages."""
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NO_OPTIONAL_PACKAGES = """
import importlib.abc
import sys
class WithoutOptionalPackages(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname.split(".")[0] in {"kivy", "torch", "transformers"}:
            raise ModuleNotFoundError("Blocked optional dependency: " + fullname)
sys.meta_path.insert(0, WithoutOptionalPackages())
"""


class MobileStartupTests(unittest.TestCase):
    def run_isolated(self, source, input_text=None):
        result = subprocess.run(
            [sys.executable, "-c", NO_OPTIONAL_PACKAGES + source],
            input=input_text, text=True, capture_output=True, cwd=ROOT,
            timeout=20,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return result.stdout

    def test_import_and_explicit_gui_error_without_kivy(self):
        self.run_isolated("""
from src.mobile.main import FelixConsole, FelixMobileApp, KIVY_AVAILABLE
assert not KIVY_AVAILABLE
assert isinstance(FelixConsole().chat_history, list)
try:
    FelixMobileApp()
except RuntimeError as exc:
    assert "FelixConsole" in str(exc)
else:
    raise AssertionError("GUI construction must explain missing Kivy")
""")

    def test_console_entrypoint_accepts_help_and_quit(self):
        output = self.run_isolated("""
import runpy
runpy.run_module("src.mobile.main", run_name="__main__")
""", "@help\nquit\n")
        self.assertIn("Comandos disponibles", output)
        self.assertIn("Hasta luego", output)


if __name__ == "__main__":
    unittest.main()
