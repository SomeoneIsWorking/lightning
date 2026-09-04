"""Repository layout and guarded cleanup ownership."""

from __future__ import annotations

import platform
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path


def host_profile() -> str:
    """Return the stable host name used for build and install directories."""

    systems = {"linux": "linux", "darwin": "macos", "win32": "windows"}
    system = systems.get(sys.platform, sys.platform.replace("/", "_"))
    machine = platform.machine().lower().replace("amd64", "x86_64")
    machine = {"arm64": "aarch64"}.get(machine, machine)
    if not machine:
        raise RuntimeError("cannot derive a build profile: platform.machine() is empty")
    return f"{system}-{machine}"


@dataclass(frozen=True)
class BuildLayout:
    """All generated paths owned by one host build."""

    repository: Path
    profile: str

    @property
    def build_root(self) -> Path:
        return self.repository / "build"

    @property
    def work(self) -> Path:
        return self.build_root / "work" / self.profile

    @property
    def install(self) -> Path:
        return self.build_root / "install" / self.profile

    @property
    def smoke(self) -> Path:
        return self.build_root / "smoke" / self.profile

    def clean(self) -> None:
        """Remove only this profile's three explicitly owned children."""

        for path in (self.work, self.install, self.smoke):
            self._remove_owned(path)

    def _remove_owned(self, path: Path) -> None:
        root = self.build_root.resolve()
        target = path.resolve()
        if target == root or root not in target.parents:
            raise RuntimeError(f"refusing cleanup outside build root: {target}")
        if target.exists():
            shutil.rmtree(target)
