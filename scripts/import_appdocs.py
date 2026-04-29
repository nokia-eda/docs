#!/usr/bin/env python3
# Copyright 2026 Nokia
# Licensed under the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause

# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "ruamel.yaml>=0.18",
# ]
# ///

"""Import app documentation from an ``edabuilder docs serve`` staging tree.

Dependencies are declared in ``pyproject.toml`` (``ruamel.yaml``). Use **uv**
from the repository root::

    uv sync
    uv run python scripts/import_appdocs.py --staging /tmp/eda-docs-XXXX
    uv run python scripts/import_appdocs.py --dry-run --staging /tmp/eda-docs-XXXX

You can also run the script path with ``uv run``; uv will create an ephemeral
environment from the inline ``# /// script`` metadata if needed::

    uv run scripts/import_appdocs.py --staging /tmp/eda-docs-XXXX

``--dry-run`` implies per-file copy/delete logging (same as ``--verbose`` for
file operations).

Staging ``docs/index.md`` (the app catalog) is ignored. App sections from
staging are merged as **siblings** under ``Apps`` (same level as NetBox, Cloud
Connect, etc.); there is no separate ``Applications`` nav wrapper.
"""

from __future__ import annotations

import argparse
import re
import shutil
import sys
from pathlib import Path
from typing import Any

try:
    from ruamel.yaml import YAML
except ImportError as exc:  # pragma: no cover
    print(
        "ruamel.yaml is required. From the docs repo root run: uv sync\n"
        "Then: uv run python scripts/import_appdocs.py ...",
        file=sys.stderr,
    )
    raise SystemExit(1) from exc

DOMAIN_PATH_RE = re.compile(r"^[a-z0-9-]+\.eda\.nokia\.com/")
# Nav entries produced by this import reference paths under apps/<domain>.eda.nokia.com/
IMPORTED_APP_NAV_PATH = re.compile(r"apps/[a-z0-9.-]+\.eda\.nokia\.com/")


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Import app docs from edabuilder staging into this MkDocs repo."
    )
    p.add_argument(
        "--staging",
        type=Path,
        required=True,
        help="Staging root (contains mkdocs.yaml or mkdocs.yml and docs/).",
    )
    p.add_argument(
        "--repo-root",
        type=Path,
        default=None,
        help="Docs repository root (default: parent of scripts/).",
    )
    p.add_argument(
        "--dry-run",
        action="store_true",
        help="Do not write files; log would-copy / would-delete per file.",
    )
    p.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Log every copy and delete. Implied for file ops when --dry-run.",
    )
    return p.parse_args()


def resolve_staging_mkdocs(staging: Path) -> Path:
    for name in ("mkdocs.yaml", "mkdocs.yml"):
        candidate = staging / name
        if candidate.is_file():
            return candidate
    raise SystemExit(f"No mkdocs.yaml or mkdocs.yml under {staging}")


def load_yaml(path: Path) -> Any:
    y = YAML(typ="rt")
    with path.open(encoding="utf-8") as f:
        return y.load(f)


def save_yaml(path: Path, data: Any, dry_run: bool) -> None:
    if dry_run:
        print(f"would write {path}")
        return
    y = YAML(typ="rt")
    y.indent(mapping=2, sequence=4, offset=2)
    with path.open("w", encoding="utf-8") as f:
        y.dump(data, f)


def find_applications_children(nav: Any) -> list[Any]:
    if not isinstance(nav, list):
        raise SystemExit("staging nav is not a list")
    for item in nav:
        if isinstance(item, dict) and "Applications" in item:
            ch = item["Applications"]
            if not isinstance(ch, list):
                raise SystemExit("Applications nav value must be a list")
            return ch
    raise SystemExit("staging nav has no Applications section")


def transform_nav_paths(applications_children: list[Any]) -> list[Any]:
    """Rewrite domain paths; drop staging ``docs/index.md`` catalog (bare ``index.md``)."""

    def transform_value(v: Any) -> Any:
        if isinstance(v, str):
            if DOMAIN_PATH_RE.match(v):
                return "apps/" + v
            return v
        if isinstance(v, list):
            return transform_list(v, is_root=False)
        if isinstance(v, dict):
            return {k: transform_value(x) for k, x in v.items()}
        return v

    def transform_list(items: list[Any], *, is_root: bool) -> list[Any]:
        out: list[Any] = []
        for el in items:
            if is_root and el == "index.md":
                continue
            if isinstance(el, str):
                out.append(transform_value(el))
            elif isinstance(el, dict):
                out.append({k: transform_value(x) for k, x in el.items()})
            else:
                out.append(el)
        return out

    return transform_list(list(applications_children), is_root=True)


def nav_subtree_references_imported_apps(obj: Any) -> bool:
    """True if any nav path string points at a generated per-app docs tree."""
    if isinstance(obj, str):
        return bool(IMPORTED_APP_NAV_PATH.search(obj))
    if isinstance(obj, list):
        return any(nav_subtree_references_imported_apps(x) for x in obj)
    if isinstance(obj, dict):
        return any(nav_subtree_references_imported_apps(x) for x in obj.values())
    return False


def discover_app_domains(staging_docs: Path) -> list[str]:
    domains: list[str] = []
    for p in sorted(staging_docs.iterdir()):
        if not p.is_dir():
            continue
        if not p.name.endswith(".eda.nokia.com"):
            continue
        docs_link = p / "docs"
        if not docs_link.exists():
            continue
        if not docs_link.is_symlink() and not docs_link.is_dir():
            continue
        try:
            resolved = docs_link.resolve()
        except OSError:
            continue
        if resolved.is_dir():
            domains.append(p.name)
    return domains


def stage(msg: str) -> None:
    print(f"==> {msg}")


def file_log(enabled: bool, msg: str) -> None:
    if enabled:
        print(msg)


def copy_file(src: Path, dst: Path, *, dry_run: bool, detail: bool, label: str) -> None:
    if detail:
        print(f"{label}: {src} -> {dst}")
    if not dry_run:
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)


def remove_path(path: Path, *, dry_run: bool, detail: bool, label: str) -> None:
    if detail:
        print(f"{label}: {path}")
    if not dry_run:
        path.unlink()


def mirror_subtree(
    src_root: Path,
    dst_root: Path,
    *,
    dry_run: bool,
    detail: bool,
    label_prefix: str,
) -> None:
    """Sync files under src_root into dst_root; delete extra files in dst_root."""
    if not src_root.is_dir():
        return
    src_files: set[Path] = set()
    for p in src_root.rglob("*"):
        if p.is_file():
            src_files.add(p.relative_to(src_root))

    for rel in sorted(src_files):
        s = src_root / rel
        d = dst_root / rel
        copy_file(s, d, dry_run=dry_run, detail=detail, label=f"{label_prefix} copy")

    if not dst_root.exists():
        return
    for p in sorted(dst_root.rglob("*"), reverse=True):
        if not p.is_file():
            continue
        rel = p.relative_to(dst_root)
        if rel not in src_files:
            remove_path(p, dry_run=dry_run, detail=detail, label=f"{label_prefix} delete")

    if not dry_run:
        for p in sorted(dst_root.rglob("*"), reverse=True):
            if p.is_dir() and not any(p.iterdir()):
                p.rmdir()


def remove_tree(path: Path, *, dry_run: bool, detail: bool, label: str) -> None:
    if detail:
        print(f"{label}: {path}")
    if not dry_run and path.exists():
        shutil.rmtree(path)


def rewrite_docs_path_prefixes_in_app_tree(app_root: Path, domain: str) -> None:
    """Turn staging paths ``docs/<domain>/...`` into repo-relative paths under ``docs/apps/``.

    MkDocs pages live under the ``docs/`` dir, but ``crd_viewer`` resolves paths from the
    project root (parent of ``mkdocs.yml``), so embedded paths must be ``docs/apps/...``.
    """
    old = f"docs/{domain}/"
    new = f"docs/apps/{domain}/"
    for md in app_root.rglob("*.md"):
        text = md.read_text(encoding="utf-8")
        if old not in text:
            continue
        md.write_text(text.replace(old, new), encoding="utf-8")


def sync_app_root_extras(
    source_app: Path,
    target_app: Path,
    *,
    dry_run: bool,
    detail: bool,
    domain: str,
) -> None:
    """Copy manifest and CRD trees from the app repo (parent of ``docs``)."""
    src_manifest = source_app / "manifest.yaml"
    dst_manifest = target_app / "manifest.yaml"
    if src_manifest.is_file():
        copy_file(
            src_manifest,
            dst_manifest,
            dry_run=dry_run,
            detail=detail,
            label=f"{domain} manifest copy",
        )
    elif dst_manifest.is_file():
        remove_path(
            dst_manifest,
            dry_run=dry_run,
            detail=detail,
            label=f"{domain} manifest delete",
        )

    src_crds = source_app / "crds"
    dst_crds = target_app / "crds"
    if src_crds.is_dir():
        mirror_subtree(
            src_crds,
            dst_crds,
            dry_run=dry_run,
            detail=detail,
            label_prefix=f"{domain}/crds",
        )
    elif dst_crds.exists():
        remove_tree(dst_crds, dry_run=dry_run, detail=detail, label=f"{domain} crds delete")


def sync_app_docs(
    source_docs: Path,
    target_docs: Path,
    *,
    dry_run: bool,
    detail: bool,
    domain: str,
) -> None:
    """Mirror index.md, vars.yaml, resources/, snippets/, media/ from source app docs tree."""
    src_vars = source_docs / "vars.yaml"
    dst_vars = target_docs / "vars.yaml"
    if src_vars.is_file():
        if not dry_run:
            target_docs.mkdir(parents=True, exist_ok=True)
        copy_file(
            src_vars,
            dst_vars,
            dry_run=dry_run,
            detail=detail,
            label=f"{domain} vars copy",
        )
    elif dst_vars.is_file():
        remove_path(
            dst_vars,
            dry_run=dry_run,
            detail=detail,
            label=f"{domain} vars delete",
        )

    src_index = source_docs / "index.md"
    dst_index = target_docs / "index.md"
    if src_index.is_file():
        if not dry_run:
            target_docs.mkdir(parents=True, exist_ok=True)
        copy_file(
            src_index,
            dst_index,
            dry_run=dry_run,
            detail=detail,
            label=f"{domain} copy",
        )
    elif dst_index.is_file():
        remove_path(
            dst_index,
            dry_run=dry_run,
            detail=detail,
            label=f"{domain} delete",
        )

    for name in ("resources", "snippets", "media"):
        s = source_docs / name
        d = target_docs / name
        if s.is_dir():
            mirror_subtree(
                s, d, dry_run=dry_run, detail=detail, label_prefix=f"{domain}/{name}"
            )
        elif d.exists():
            remove_tree(
                d,
                dry_run=dry_run,
                detail=detail,
                label=f"{domain} delete tree",
            )


def merge_flat_app_nav_into_mkdocs_nav(
    nav: list[Any], flat_nav_entries: list[Any]
) -> None:
    """Splice staging app sections into ``Apps`` as siblings (no ``Applications`` wrapper).

    Removes prior import output: legacy ``Applications`` blocks, and any
    single-key dict whose subtree only references generated ``*.eda.nokia.com``
    app paths (so manual pages like ``Protocols: apps/protocols.md`` stay).
    """
    for item in nav:
        if isinstance(item, dict) and "Apps" in item:
            apps_children = item["Apps"]
            if not isinstance(apps_children, list):
                raise SystemExit("Apps nav entry must be a list")

            def should_drop_imported(c: Any) -> bool:
                if isinstance(c, dict) and "Applications" in c:
                    return True
                if isinstance(c, dict) and len(c) == 1:
                    return nav_subtree_references_imported_apps(c)
                return False

            apps_children[:] = [c for c in apps_children if not should_drop_imported(c)]
            apps_children.extend(flat_nav_entries)
            return
    raise SystemExit("nav has no Apps section")


def prune_orphan_app_trees(
    docs_dir: Path,
    keep_domains: set[str],
    *,
    dry_run: bool,
    detail: bool,
) -> int:
    """Remove ``docs/apps/<domain>.eda.nokia.com/`` not in staging. Returns count removed."""
    apps_root = docs_dir / "apps"
    if not apps_root.is_dir():
        return 0
    removed = 0
    for p in sorted(apps_root.iterdir()):
        if not p.is_dir():
            continue
        if not p.name.endswith(".eda.nokia.com"):
            continue
        if p.name in keep_domains:
            continue
        if detail:
            print(f"prune removed app tree: {p}")
        if not dry_run:
            shutil.rmtree(p)
        removed += 1
    return removed


def main() -> None:
    args = parse_args()
    staging = args.staging.resolve()
    repo_root = (
        args.repo_root.resolve()
        if args.repo_root
        else Path(__file__).resolve().parent.parent
    )
    dry_run: bool = args.dry_run
    file_detail: bool = bool(args.verbose or dry_run)

    staging_mkdocs = resolve_staging_mkdocs(staging)
    staging_docs = staging / "docs"
    if not staging_docs.is_dir():
        raise SystemExit(f"Missing staging docs dir: {staging_docs}")

    repo_docs = repo_root / "docs"
    mkdocs_yml = repo_root / "mkdocs.yml"
    if not mkdocs_yml.is_file():
        raise SystemExit(f"Missing {mkdocs_yml}")

    stage("load staging nav")
    staging_data = load_yaml(staging_mkdocs)
    nav_staging = staging_data.get("nav")
    if nav_staging is None:
        raise SystemExit("staging mkdocs has no nav")
    applications_children = find_applications_children(nav_staging)
    transformed_children = transform_nav_paths(applications_children)

    stage("discover applications")
    domains = discover_app_domains(staging_docs)
    print(f"discovered {len(domains)} app(s): {', '.join(domains)}")

    stage("sync doc trees")
    for domain in domains:
        app_staging = staging_docs / domain / "docs"
        try:
            source_docs = app_staging.resolve()
        except OSError as e:
            print(f"warn: skip {domain}: cannot resolve docs: {e}", file=sys.stderr)
            continue
        if not source_docs.is_dir():
            print(f"warn: skip {domain}: not a directory: {source_docs}", file=sys.stderr)
            continue
        target_docs = repo_docs / "apps" / domain / "docs"
        target_app = repo_docs / "apps" / domain
        sync_app_docs(
            source_docs,
            target_docs,
            dry_run=dry_run,
            detail=file_detail,
            domain=domain,
        )
        source_app = source_docs.parent
        sync_app_root_extras(
            source_app,
            target_app,
            dry_run=dry_run,
            detail=file_detail,
            domain=domain,
        )
        if not dry_run:
            rewrite_docs_path_prefixes_in_app_tree(target_app, domain)

    stage("merge app nav into mkdocs.yml")
    mkdocs_data = load_yaml(mkdocs_yml)
    nav_main = mkdocs_data.get("nav")
    if not isinstance(nav_main, list):
        raise SystemExit("mkdocs.yml nav must be a list")
    merge_flat_app_nav_into_mkdocs_nav(nav_main, transformed_children)
    save_yaml(mkdocs_yml, mkdocs_data, dry_run)

    stage("prune removed app trees")
    n_pruned = prune_orphan_app_trees(
        repo_docs, set(domains), dry_run=dry_run, detail=file_detail
    )
    if n_pruned == 0:
        print("no orphan app trees to prune")
    else:
        verb = "would prune" if dry_run else "pruned"
        print(f"{verb} {n_pruned} orphan app tree(s)")

    stage("done")


if __name__ == "__main__":
    main()
