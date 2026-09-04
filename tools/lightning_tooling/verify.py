"""Installed-consumer and repository policy verification."""

from __future__ import annotations

import re
from pathlib import Path

from .build import LightningBuilder
from .process import require_program, run


def verify_installed_consumer(builder: LightningBuilder) -> None:
    """Compile and execute the shipping installed-library boundary."""

    layout = builder.layout
    layout.smoke.mkdir(parents=True, exist_ok=True)
    executable = layout.smoke / "install_contract"
    compiler = require_program(builder.options.compiler)
    run(
        [
            compiler,
            builder.repository / "tests" / "install_contract.c",
            "-Wall",
            "-Wextra",
            "-Werror",
            f"-I{layout.install / 'include'}",
            layout.install / "lib" / "liblightning.a",
            "-ldl",
            "-pthread",
            "-o",
            executable,
        ],
        cwd=builder.repository,
    )
    run([executable], cwd=builder.repository)
    print("installed consumer: emitted native function returned 42")


def verify_maintainer_scripts_are_python(repository: Path) -> None:
    """Keep new portfolio tooling Python without policing upstream scripts."""

    files = sorted(
        path
        for path in (repository / "tools").rglob("*")
        if path.is_file() and "__pycache__" not in path.parts
    )
    scripts = [path for path in files if path.suffix != ".py"]
    if scripts:
        raise RuntimeError(
            "maintainer tools contain non-Python files: "
            + ", ".join(str(path.relative_to(repository)) for path in scripts)
        )
    print(f"maintainer script policy: {len(files)} file(s), 0 non-Python files")


def verify_ci_contract(repository: Path) -> None:
    """Check the one truthful hosted platform job cannot silently weaken."""

    workflow = repository / ".github" / "workflows" / "ci.yml"
    text = workflow.read_text(encoding="utf-8")
    required = (
        "runs-on: ubuntu-24.04",
        "timeout-minutes:",
        "fetch-depth: 0",
        "persist-credentials: false",
        "permissions:\n  contents: read",
        "tools/verify.py",
        "--cc clang",
    )
    missing = [item for item in required if item not in text]
    action_uses = re.findall(r"uses:\s*([^\s]+)", text)
    unpinned = [use for use in action_uses if not re.search(r"@[0-9a-f]{40}$", use)]
    runner_count = len(re.findall(r"^\s+runs-on:\s*", text, flags=re.MULTILINE))
    if missing or unpinned or runner_count != 1:
        raise RuntimeError(
            f"CI contract invalid: missing={missing or 'none'}, "
            f"unpinned={unpinned or 'none'}, host_jobs={runner_count}"
        )
    print(
        f"CI contract: 1 executable host job, {len(action_uses)} immutable action pin(s)"
    )
