from datetime import datetime
from pathlib import Path
import yaml
from mkdocs.plugins import event_priority


# Priority 100 makes this run before the macros plugin's on_config, so the
# version values added to config.extra below are copied into the macro
# variables and become usable in markdown (e.g. -{{ eda_major_version }}-).
@event_priority(100)
def on_config(config, **kwargs):
    # set current_year in the copyright
    current_year = datetime.now().year
    if config.copyright:
        config.copyright = config.copyright.format(current_year=current_year)

    # Note: only present in the docs.eda.dev site
    eda_version = config.extra.get("eda_version")
    if eda_version:
        eda_major_version = f"{eda_version.split('.')[0]}"
        eda_minor_version = f"{eda_version.split('.')[1]}"
        eda_major_minor_version = f"{eda_major_version}.{eda_minor_version}"
        config.edit_uri = config.edit_uri.format(
            versioned_branch="release-" + eda_major_minor_version
        )

        # expose the derived versions as macro variables via config.extra
        config.extra["eda_major_version"] = eda_major_version
        config.extra["eda_minor_version"] = eda_minor_version
        config.extra["eda_major_minor_version"] = eda_major_minor_version
        config.extra["eda_year"] = 2000 + int(eda_major_version)  # e.g. 24 -> 2024

        # expose the derived versions as macro variables via config.extra
        config.extra["eda_major_version"] = eda_major_version
        config.extra["eda_minor_version"] = eda_minor_version
        config.extra["eda_major_minor_version"] = eda_major_minor_version
        config.extra["eda_year"] = 2000 + int(eda_major_version)  # e.g. 24 -> 2024


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

    cfg_path = Path(config.config_file_path).resolve()

    url_parts = Path(str(page.url)).parts
    if len(url_parts) == 0:
        return markdown

    apps_path = config.get("extra", {}).get("apps_path")

    if "resources" in url_parts:
        idx = url_parts.index("resources")
        app_id = url_parts[idx - 2]
    else:
        app_id = url_parts[len(url_parts) - 2]

    # docs.eda.dev uses 'apps' before app_id
    manifest_path = (cfg_path.parent / apps_path / app_id / "manifest.yaml").resolve()

    icon = _compute_crd_icon(manifest_path, resource_plural)
    meta["icon"] = icon
    page.meta = meta

    return markdown
