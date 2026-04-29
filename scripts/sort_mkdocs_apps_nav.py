#!/usr/bin/env python3
# Copyright 2026 Nokia
# Licensed under the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause

# /// script
# requires-python = ">=3.11"
# ///

"""Alphabetically sort top-level entries under the ``Apps`` nav section in ``mkdocs.yml``.

Nested children under each Apps entry are left unchanged. Run from the repo root::

    uv run scripts/sort_mkdocs_apps_nav.py
    uv run scripts/sort_mkdocs_apps_nav.py --dry-run

Sort key is the nav label (text before ``:``), case-insensitive; bare paths (e.g.
``apps/index.md``) sort by the full path string. When two entries share the same
label (e.g. two ``Protocols`` items), the path on the same line (if any) breaks the tie.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


def parse_args() -> argparse.Namespace:
    root = Path(__file__).resolve().parent.parent
    p = argparse.ArgumentParser(
        description="Sort top-level items under nav → Apps in mkdocs.yml (nested nav unchanged)."
    )
    p.add_argument(
        "mkdocs_yml",
        type=Path,
        nargs="?",
        default=root / "mkdocs.yml",
        help="Path to mkdocs.yml (default: <repo>/mkdocs.yml)",
    )
    p.add_argument(
        "--dry-run",
        action="store_true",
        help="Print sorted first lines only; do not write the file.",
    )
    return p.parse_args()


def sort_key(block: str) -> tuple[str, str]:
    first = block.split("\n", 1)[0].strip()
    if not first.startswith("- "):
        msg = f"Expected block to start with '- ', got: {first[:80]!r}"
        raise ValueError(msg)
    rest = first[2:].strip()
    if ":" in rest:
        title, _, rhs = rest.partition(":")
        return (title.strip().lower(), rhs.strip().lower())
    return (rest.lower(), "")


def sort_apps_nav(lines: list[str]) -> tuple[int, int, list[str]] | None:
    """Return (start_line, end_line, sorted_blocks) or None if Apps section missing."""
    start: int | None = None
    for i, line in enumerate(lines):
        if line.startswith("  - Apps:"):
            start = i
            break
    if start is None:
        return None

    end: int | None = None
    for i in range(start + 1, len(lines)):
        line = lines[i]
        if line.startswith("  - ") and not line.startswith("    "):
            end = i
            break
    if end is None:
        return None

    body = lines[start + 1 : end]
    blocks: list[str] = []
    i = 0
    while i < len(body):
        line = body[i]
        if line.startswith("      - "):
            block_lines = [line]
            i += 1
            while i < len(body) and not body[i].startswith("      - "):
                block_lines.append(body[i])
                i += 1
            blocks.append("".join(block_lines))
        else:
            i += 1

    sorted_blocks = sorted(blocks, key=sort_key)
    return start, end, sorted_blocks


def main() -> int:
    args = parse_args()
    path: Path = args.mkdocs_yml
    if not path.is_file():
        print(f"Not a file: {path}", file=sys.stderr)
        return 1

    text = path.read_text(encoding="utf-8")
    lines = text.splitlines(keepends=True)
    result = sort_apps_nav(lines)
    if result is None:
        print("Could not find Apps nav section or its closing boundary.", file=sys.stderr)
        return 1
    start, end, sorted_blocks = result

    if args.dry_run:
        print(f"{path}: would sort {len(sorted_blocks)} top-level Apps entries (lines {start + 2}-{end}):")
        for b in sorted_blocks:
            print(f"  {b.splitlines()[0].rstrip()}")
        return 0

    new_lines = lines[: start + 1] + sorted_blocks + lines[end:]
    path.write_text("".join(new_lines), encoding="utf-8")
    print(f"Wrote {path}: sorted {len(sorted_blocks)} top-level Apps nav entries.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
