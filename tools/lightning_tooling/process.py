"""Checked subprocess boundary with actionable missing-tool failures."""

from __future__ import annotations

import os
import shutil
import subprocess
from collections.abc import Mapping, Sequence
from pathlib import Path


_INSTALL_HINTS = {
    "autoreconf": "sudo dnf install autoconf automake (Fedora), sudo apt install autoconf automake (Ubuntu) "
    "or brew install autoconf automake (macOS)",
    "libtoolize": "sudo dnf install libtool (Fedora), sudo apt install libtool (Ubuntu) or brew install libtool (macOS)",
    "make": "sudo dnf install make (Fedora) or sudo apt install make (Ubuntu)",
}

# Homebrew installs GNU libtoolize as glibtoolize beside Apple's unrelated libtool; gnulib's bootstrap looks
# for both names.
_ALIASES = {
    "libtoolize": ("libtoolize", "glibtoolize"),
}


def require_program(program: str) -> str:
    """Resolve a program or refuse with the exact native-package command."""

    for name in _ALIASES.get(program, (program,)):
        resolved = shutil.which(name)
        if resolved is not None:
            return resolved
    hint = _INSTALL_HINTS.get(program, f"install {program} with the platform package manager")
    raise RuntimeError(f"required program '{program}' is missing; {hint}")


def run(
    command: Sequence[str | Path],
    *,
    cwd: Path,
    environment: Mapping[str, str] | None = None,
) -> None:
    """Run one command and propagate failure without fallback or retry."""

    env = os.environ.copy()
    if environment is not None:
        env.update(environment)
    rendered = [str(part) for part in command]
    print(f"+ ({cwd}) {' '.join(rendered)}", flush=True)
    subprocess.run(rendered, cwd=cwd, env=env, check=True)


def output(command: Sequence[str | Path], *, cwd: Path) -> str:
    """Return checked command output with no silent empty fallback."""

    rendered = [str(part) for part in command]
    completed = subprocess.run(
        rendered,
        cwd=cwd,
        check=True,
        capture_output=True,
        text=True,
    )
    result = completed.stdout.strip()
    if not result:
        raise RuntimeError(f"command returned empty output: {' '.join(rendered)}")
    return result
