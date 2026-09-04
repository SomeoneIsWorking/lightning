"""Falsifiers for build-directory ownership and host naming."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from lightning_tooling.layout import BuildLayout, host_profile


class BuildLayoutTests(unittest.TestCase):
    def test_clean_removes_only_selected_profile(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repository = Path(temporary)
            selected = BuildLayout(repository, "linux-x86_64")
            sibling = BuildLayout(repository, "macos-aarch64")
            for path in (selected.work, selected.install, selected.smoke, sibling.work):
                path.mkdir(parents=True)
                (path / "marker").write_text("owned", encoding="utf-8")

            selected.clean()

            self.assertFalse(selected.work.exists())
            self.assertFalse(selected.install.exists())
            self.assertFalse(selected.smoke.exists())
            self.assertTrue((sibling.work / "marker").is_file())

    def test_host_profile_has_system_and_machine(self) -> None:
        profile = host_profile()
        self.assertIn("-", profile)
        self.assertNotEqual(profile.rsplit("-", 1)[-1], "")

    def test_clean_refuses_profile_that_resolves_to_build_root(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            layout = BuildLayout(Path(temporary), "..")
            with self.assertRaisesRegex(RuntimeError, "refusing cleanup"):
                layout.clean()


if __name__ == "__main__":
    unittest.main()
