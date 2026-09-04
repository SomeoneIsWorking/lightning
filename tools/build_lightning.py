#!/usr/bin/env python3
"""Build and install the maintained GNU lightning dependency."""

from __future__ import annotations

import argparse

from lightning_tooling.cli import add_build_arguments, builder_from_arguments


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    add_build_arguments(parser)
    builder = builder_from_arguments(parser.parse_args())
    prefix = builder.build()
    print(f"GNU lightning install prefix: {prefix}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
