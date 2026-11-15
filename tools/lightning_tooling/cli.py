"""Command-line interface shared by build and verification entry points."""

from __future__ import annotations

import argparse
import os
from pathlib import Path

from .build import BuildOptions, LightningBuilder
from .layout import BuildLayout, cross_profile, host_profile


def repository_root() -> Path:
    return Path(__file__).resolve().parents[2]


def add_build_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--cc", default=os.environ.get("CC", "cc"), help="C compiler")
    parser.add_argument(
        "--jobs",
        type=int,
        default=max(1, os.cpu_count() or 1),
        help="parallel make jobs",
    )
    parser.add_argument("--clean", action="store_true", help="clean this host profile first")
    parser.add_argument("--host", help="GNU target triple to cross-compile for, e.g. x86_64-w64-mingw32")
    parser.add_argument(
        "--skip-upstream-tests",
        action="store_true",
        help="build/install only; the complete verifier never uses this",
    )


def builder_from_arguments(arguments: argparse.Namespace) -> LightningBuilder:
    profile = cross_profile(arguments.host) if arguments.host else host_profile()
    layout = BuildLayout(repository_root(), profile)
    options = BuildOptions(
        compiler=arguments.cc,
        jobs=arguments.jobs,
        clean=arguments.clean,
        run_upstream_tests=not arguments.skip_upstream_tests,
        host=arguments.host,
    )
    return LightningBuilder(layout, options)
