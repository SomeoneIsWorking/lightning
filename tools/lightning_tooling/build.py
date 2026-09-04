"""Deterministic GNU lightning configure, test, and install orchestration."""

from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path

from .layout import BuildLayout
from .process import output, require_program, run


@dataclass(frozen=True)
class BuildOptions:
    """Inputs that can affect the generated host library."""

    compiler: str
    jobs: int
    clean: bool = False
    run_upstream_tests: bool = True


class LightningBuilder:
    """Own the complete build-to-installed-prefix transition."""

    def __init__(self, layout: BuildLayout, options: BuildOptions) -> None:
        if options.jobs < 1:
            raise ValueError("jobs must be at least one")
        self.layout = layout
        self.options = options

    def build(self) -> Path:
        """Build, optionally test, and install a static development prefix."""

        if self.options.clean:
            self.layout.clean()
        self._require_tools()
        self._ensure_gnulib()
        self._bootstrap()
        self._configure()
        self._make_library()
        if self.options.run_upstream_tests:
            self._test_library()
        self._install_library()
        self.verify_install_shape()
        return self.layout.install

    def verify_install_shape(self) -> None:
        """Refuse an incomplete prefix instead of reporting a partial install."""

        required = (
            self.layout.install / "include" / "lightning.h",
            self.layout.install / "lib" / "liblightning.a",
            self.layout.install / "lib" / "pkgconfig" / "lightning.pc",
        )
        missing = [path for path in required if not path.is_file()]
        architecture_headers = sorted(
            (self.layout.install / "include" / "lightning").glob("jit_*.h")
        )
        if missing or not architecture_headers:
            details = [str(path) for path in missing]
            if not architecture_headers:
                details.append(
                    str(self.layout.install / "include" / "lightning" / "jit_*.h")
                )
            raise RuntimeError(f"incomplete GNU lightning install: missing {details}")
        print(
            "install contract: "
            f"{len(required)}/{len(required)} core files and "
            f"{len(architecture_headers)} architecture header(s) present"
        )

    @property
    def repository(self) -> Path:
        return self.layout.repository

    def _require_tools(self) -> None:
        for program in ("git", "autoreconf", "libtoolize", "make"):
            require_program(program)
        require_program(self.options.compiler)

    def _ensure_gnulib(self) -> None:
        expected = output(["git", "rev-parse", "HEAD:gnulib"], cwd=self.repository)
        gnulib = self.repository / "gnulib"
        actual = ""
        if gnulib.is_dir():
            try:
                actual = output(["git", "rev-parse", "HEAD"], cwd=gnulib)
            except subprocess.CalledProcessError:
                actual = ""
        if actual != expected:
            run(
                ["git", "submodule", "update", "--init", "--checkout", "gnulib"],
                cwd=self.repository,
            )
            actual = output(["git", "rev-parse", "HEAD"], cwd=gnulib)
        if actual != expected:
            raise RuntimeError(
                f"gnulib revision mismatch: expected {expected}, found {actual or 'none'}"
            )
        print(f"gnulib revision: {actual}")

    def _bootstrap(self) -> None:
        run([self.repository / "bootstrap", "--no-bootstrap-sync"], cwd=self.repository)
        configure = self.repository / "configure"
        if not configure.is_file():
            raise RuntimeError(f"bootstrap completed without generating {configure}")

    def _configure(self) -> None:
        self.layout.work.mkdir(parents=True, exist_ok=True)
        self.layout.install.mkdir(parents=True, exist_ok=True)
        run(
            [
                self.repository / "configure",
                f"--prefix={self.layout.install}",
                "--disable-shared",
                "--enable-static",
                "--disable-disassembler",
                "CFLAGS=-O2 -g -fno-omit-frame-pointer",
            ],
            cwd=self.layout.work,
            environment={"CC": require_program(self.options.compiler)},
        )

    def _make_library(self) -> None:
        run(
            ["make", "-C", self.layout.work / "lib", f"-j{self.options.jobs}"],
            cwd=self.repository,
        )

    def _test_library(self) -> None:
        run(
            [
                "make",
                "-C",
                self.layout.work / "check",
                "check",
                f"-j{self.options.jobs}",
            ],
            cwd=self.repository,
        )

    def _install_library(self) -> None:
        for relative, target in (
            ("include", "install"),
            ("lib", "install"),
            (".", "install-pkgconfiglibDATA"),
        ):
            directory = self.layout.work if relative == "." else self.layout.work / relative
            run(["make", "-C", directory, target], cwd=self.repository)
