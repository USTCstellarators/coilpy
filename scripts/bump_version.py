#!/usr/bin/env python3
"""Bump the project version across the repository."""

from __future__ import annotations

import argparse
import pathlib
import re
import sys


ROOT = pathlib.Path(__file__).resolve().parents[1]
INIT_FILE = ROOT / "coilpy" / "__init__.py"
MESON_FILE = ROOT / "meson.build"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--part",
        choices=("major", "minor", "patch"),
        default="patch",
        help="Version component to increment.",
    )
    return parser.parse_args()


def bump(version: str, part: str) -> str:
    major, minor, patch = [int(item) for item in version.split(".")]
    if part == "major":
        major += 1
        minor = 0
        patch = 0
    elif part == "minor":
        minor += 1
        patch = 0
    else:
        patch += 1
    return f"{major}.{minor}.{patch}"


def replace_version(path: pathlib.Path, pattern: str, replacement: str) -> str:
    content = path.read_text()
    updated, count = re.subn(pattern, replacement, content, count=1, flags=re.MULTILINE)
    if count != 1:
        raise RuntimeError(f"Unable to update version in {path}")
    path.write_text(updated)
    return updated


def main() -> int:
    args = parse_args()
    init_content = INIT_FILE.read_text()
    match = re.search(r'^__version__ = "(\d+\.\d+\.\d+)"$', init_content, re.MULTILINE)
    if match is None:
        raise RuntimeError(f"Unable to find __version__ in {INIT_FILE}")

    current = match.group(1)
    new_version = bump(current, args.part)

    replace_version(
        INIT_FILE,
        r'^__version__ = "\d+\.\d+\.\d+"$',
        f'__version__ = "{new_version}"',
    )
    replace_version(
        MESON_FILE,
        r"version : '\d+\.\d+\.\d+'",
        f"version : '{new_version}'",
    )

    print(new_version)
    return 0


if __name__ == "__main__":
    sys.exit(main())
