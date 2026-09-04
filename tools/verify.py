#!/usr/bin/env python3
"""Run the maintained GNU lightning asset-free landing gate."""

from __future__ import annotations

import argparse
import sys

from lightning_tooling.cli import add_build_arguments, builder_from_arguments, repository_root
from lightning_tooling.process import run
from lightning_tooling.verify import (
    verify_ci_contract,
    verify_installed_consumer,
    verify_maintainer_scripts_are_python,
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    add_build_arguments(parser)
    arguments = parser.parse_args()
    if arguments.skip_upstream_tests:
        parser.error("the complete verifier cannot skip GNU lightning's upstream tests")

    repository = repository_root()
    verify_maintainer_scripts_are_python(repository)
    verify_ci_contract(repository)
    run(
        [
            sys.executable,
            "-m",
            "unittest",
            "discover",
            "-s",
            "tools/tests",
            "-t",
            "tools",
            "-v",
        ],
        cwd=repository,
    )
    builder = builder_from_arguments(arguments)
    builder.build()
    verify_installed_consumer(builder)
    print("GNU lightning verification passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
