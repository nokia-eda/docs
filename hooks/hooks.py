from datetime import datetime
from pathlib import Path

import yaml


def on_config(config, **kwargs):
    # set current_year in the copyright
    current_year = datetime.now().year
    config.copyright = config.copyright.format(current_year=current_year)

    # set the versioned docs branch
    eda_version = config.extra["eda_version"]
    eda_major_version = f"{eda_version.split('.')[0]}"
    eda_minor_version = f"{eda_version.split('.')[1]}"
    eda_major_minor_version = f"{eda_major_version}.{eda_minor_version}"
    config.edit_uri = config.edit_uri.format(
        versioned_branch="release-" + eda_major_minor_version
    )


def _compute_crd_icon(manifest_file: Path, resource_plural: str) -> str:
    """Return a Material icon id for a CRD: workflow CRDs use graph-outline, else code-json."""
    if not manifest_file.exists():
        return "material/code-json"  # sensible default/fallback

    data = yaml.safe_load(manifest_file.read_text()) or {}
    components = data.get("spec", {}).get("components", [])
    app_id = data.get("spec", {}).get("group", "")

    for c in components:
        crd = c.get("crd") or {}
        if not crd:
            continue

        if f"{app_id}_{resource_plural}.yaml" not in crd.get("path"):
            continue

        return (
            "material/graph-outline"
            if crd.get("workflow", False)
            else "material/code-json"
        )

    return "material/code-json"


def on_page_markdown(markdown, page, config, files):
    """Replace front matter ``icon: auto-crd`` with a concrete icon from the app manifest."""
    meta = page.meta or {}

    # Only compute when icon is set to auto-crd
    if meta.get("icon") != "auto-crd":
        return markdown

    resource_plural = meta.get("resource_name_plural")
    if not resource_plural:
        return markdown

    cfg = Path(config.config_file_path).resolve()

    url = Path(str(page.url))
    if len(url.parts) == 0:
        return markdown

    app_id = Path(str(page.url)).parts[1]

    manifest_path = (cfg.parent / "docs" / "apps" / app_id / "manifest.yaml").resolve()

    icon = _compute_crd_icon(manifest_path, resource_plural)
    meta["icon"] = icon
    page.meta = meta

    return markdown
