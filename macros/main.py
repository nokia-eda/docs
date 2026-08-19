# Copyright 2025 Nokia
# Licensed under the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause
"""
Mkdocs-macros module
"""

import posixpath
from dataclasses import dataclass, field
from pathlib import Path

import yaml


def _scale_to_width_percent(scale):
    """Return a CSS width percentage from a numeric scale factor, or None.

    ``scale`` is a multiplier on the container width: ``0.5`` → ``50%``,
    ``2`` → ``200%``. ``1`` means natural layout (no width style). Empty
    string is treated like the default. Only ``int``/``float`` are accepted
    (booleans and other types are ignored).
    """
    if scale is None or scale == "":
        return None
    if isinstance(scale, bool):
        return None
    if not isinstance(scale, (int, float)):
        return None
    if scale <= 0:
        return None
    if scale == 1:
        return None
    pct = scale * 100.0
    if pct.is_integer():
        return f"{int(pct)}%"
    return f"{pct:g}%"


def _normalize_path(path, env):
    """Turn a path relative to the current markdown file into a URL relative to the built HTML.

    With ``use_directory_urls``, ``page.md`` becomes ``page/index.html`` while
    ``section/index.md`` stays ``section/index.html``.  Raw HTML in macros is not
    rewritten like Markdown image URLs, so the correct relative URL must be derived
    from ``File.dest_path`` for the page and the asset.

    A single leading ``/`` is treated as docs-root (``src_path`` under the docs dir),
    so ``/javascripts/foo.js`` resolves like a relative URL for versioned ``site_url``
    deploys. Protocol-relative URLs (``//host/...``) are left unchanged.
    """
    if not path:
        return path
    if path.startswith(("http://", "https://", "#")):
        return path
    if path.startswith("//"):
        return path

    page_file = env.page.file
    # mkdocs-macros attaches MkDocs' Files collection in on_nav (see plugin on_nav).
    try:
        files = env.variables["files"]
    except (TypeError, KeyError, AttributeError):
        files = None
    if files is None:
        return path

    if path.startswith("/"):
        resolved_src = posixpath.normpath(path[1:])
        if not resolved_src or resolved_src == ".":
            return path
    else:
        page_src_dir = posixpath.dirname(page_file.src_path)
        resolved_src = posixpath.normpath(posixpath.join(page_src_dir, path))

    asset = files.get_file_from_path(resolved_src)
    if asset is None:
        return path
    page_dest_dir = posixpath.dirname(page_file.dest_path) or "."
    rel = posixpath.relpath(asset.dest_path, page_dest_dir)

    return rel.replace("\\", "/")


def define_env(env):
    """
    Macros used in Nokia EDA documentation
    """

    @env.macro
    def diagram(url="", path="", page=0, title="", zoom=2):
        """
        Diagram macro. URL can be a local file `path` that starts with a ./ (dot) or ../ (dot-dot) prefix
        or a remote URL `url` that starts with http or https or a shorthand syntax for drawio files kept in a GitHub repo.
        """

        _location = ""

        # to allow shorthand syntax for drawio URLs, like:
        # srl-labs/srlinux-getting-started/main/diagrams/topology.drawio
        # we will append the missing prefix to it if it doesn't start with http already
        if not url.startswith("http"):
            _location = "https://raw.githubusercontent.com/" + url

        if path:
            _location = _normalize_path(path, env)

        diagram_tmpl = f"""
    <figure>
        <div class='mxgraph'
                style='max-width:100%;border:1px solid transparent;margin:0 auto; display:block; box-shadow: 0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1); border-radius: 0.25rem;'
                data-mxgraph='{{"url":"{_location}","page":{page},"zoom":{zoom},"highlight":"#0000ff","nav":true,"resize":false,"auto-fit":true,"allow-zoom-out":true,"edit":"_blank","dark-mode":false}}'>
        </div>
        {f"<figcaption>{title}</figcaption>" if title else ""}
    </figure>
    """

        return diagram_tmpl

    @env.macro
    def video(url, title=""):
        """
        HTML5 video macro
        """

        url = _normalize_path(url, env)

        video_tmpl = f"""
<figure>
<video style="overflow: hidden; box-shadow: 0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1); border-radius: 0.25rem;" width="100%" controls playsinline>
    <source src="{url}" type="video/mp4">
</video>
{f"<figcaption>{title}</figcaption>" if title else ""}
</figure>
"""

        return video_tmpl

    @env.macro
    def youtube(url):
        """
        Youtube video macro
        """

        video_tmpl = f"""
<div class="iframe-container" >
<iframe style="box-shadow: 0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1); border-radius: 0.25rem;" src="{url}" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>
</div>
"""

        return video_tmpl

    @env.macro
    def js_script(src: str) -> str:
        """Emit a script tag with ``src`` rewritten for the built page (supports docs-root ``/…`` paths)."""
        url = _normalize_path(src, env)
        return f'<script type="text/javascript" src="{url}" async></script>'

    @env.macro
    def image(
        url="",
        light_url="",
        dark_url="",
        padding=0,
        border_radius=0.0,
        shadow=False,
        center=True,
        scale=1,
        title="",
    ):
        """
        Image macro with dot background.

        Parameters:
            url (str): Image URL. Used for both light and dark modes if no specific URLs are provided.
            light_url (str): Image URL for light mode.
            dark_url (str): Image URL for dark mode.
            padding (int): Padding around the image (in px). Default is 0.
            border_radius (float): Border radius for the image (in rem). Default is 0.0.
            shadow (bool): Whether to apply a shadow to the image. Default is False.
            center (bool): Whether to center the image in the figure. Default is True.
            scale (int | float): Width as a multiple of the container width: ``1`` is default
                (no extra width; natural size). ``0.5`` is half, ``2`` is double. Non-numeric
                values, non-positive values, and ``1`` apply no width override.
            title (str): Optional caption/title for the image. Default is "".
        """
        url = _normalize_path(url, env)
        light_url = _normalize_path(light_url, env)
        dark_url = _normalize_path(dark_url, env)

        scale_width = _scale_to_width_percent(scale)
        img_scale_style = (
            f' style="width: {scale_width}; height: auto;"' if scale_width else ""
        )

        if shadow:
            img_class = "img-shadow"
        else:
            img_class = ""

        # if only one url is provided the image is used for both light and dark modes
        img_src = (
            f'<img src="{url}" class="{img_class}"{img_scale_style} alt="{title}">'
        )

        # if light and dark url are provided
        if light_url and dark_url:
            # data-proofer-ignore is used to ignore the htmltest checking for #only-light and #only-dark hashes
            # that do not exist
            img_src = (
                f'<img data-proofer-ignore src="{light_url}#only-light" class="{img_class}"{img_scale_style} alt="{title}">'
                f'<img data-proofer-ignore src="{dark_url}#only-dark" class="{img_class}"{img_scale_style} alt="{title}">'
            )

        # Compute base style
        base_style = f"border-radius: {border_radius}rem; position: relative; display: inline-block;"
        if center:
            center_style = "text-align: center; width: 100%;"
        else:
            center_style = ""
        div_style = f"padding: {padding}px; {base_style} {center_style}".strip()
        # remove bottom padding when figure is used since figcaption adds its own spacing
        figure_style = f"padding: {padding}px {padding}px 0 {padding}px; {base_style} {center_style}".strip()

        # if title is provided, use figure element with figcaption inside the polka div
        if title:
            image_tmpl = (
                f'<figure class="polka" style="{figure_style}">{img_src}'
                f"<figcaption>{title}</figcaption></figure>"
            )
        else:
            image_tmpl = f'<div class="polka" style="{div_style}">{img_src}</div>'

        return image_tmpl

    @dataclass
    class OSVersions:
        """Collect supported OS/vendor versions from a manifest for HTML output."""

        versions: dict[str, list[str]] = field(default_factory=dict)

        def add_version(self, vendor: str, version: str):
            """Record one version string under a display vendor name."""
            if vendor not in self.versions:
                self.versions[vendor] = []
            self.versions[vendor].append(version)

        def format_versions(self) -> str:
            """Return a small HTML blurb of vendors and versions, or ``N/A`` if empty."""
            result = ""
            for vendor, vers in self.versions.items():
                result += f"<strong>{vendor}:</strong> {', '.join(vers)} <br/>"
            if result == "":
                return "N/A"
            return result

    @env.macro
    def supported_os_versions(_: str = None, manifest: str = "manifest.yaml") -> str:
        """Return the string with the supported OSes extracted from the manifest.

        Provided by its path.
        """
        vendor_map = {
            "srl": "Nokia SR Linux",
            "sros": "Nokia SR OS",
            "eos": "Arista EOS",
            "nxos": "Cisco NX-OS",
        }
        os_versions = OSVersions()

        p = _get_app_file(manifest)
        if not p.exists():
            return f"file does not exist: {p.absolute()}"

        with open(p.absolute()) as f:
            manifest_data = yaml.safe_load(f)

        endpoints = manifest_data.get("spec", {}).get("supportedEndpoints", [])
        for entry in endpoints:
            # entry format: "vendor:version[:extra]"
            parts = entry.split(":")
            if len(parts) >= 2:
                vendor_key = parts[0]
                version_str = ":".join(parts[1:])
                vendor_name = vendor_map.get(vendor_key)
                if vendor_name:
                    os_versions.add_version(
                        # replace * in version_str with \* to escape it in markdown
                        # else it is interpreted as an italic symbol
                        vendor_name,
                        version_str.replace("*", r"\*"),
                    )

        return os_versions.format_versions()

    @env.macro
    def category(resource_plural: str, manifest: str = "manifest.yaml") -> str:
        """Returns the UI category of an app's CRD by looking it up in its corresponding manifest file."""
        p = _get_app_file(manifest)
        if not p.exists():
            return f"file does not exist: {p.absolute()}"

        with open(p.absolute()) as f:
            manifest_data = yaml.safe_load(f)

        app_id = manifest_data.get("spec", {}).get("group", "")
        components = manifest_data.get("spec", {}).get("components", [])

        for c in components:
            crd = c.get("crd", {})
            if not crd:
                continue

            if f"{app_id}_{resource_plural}.yaml" not in crd.get("path"):
                continue

            if crd.get("workflow", False):
                return "Workflows"

            return crd.get("ui", {}).get("category", "")

        return ""

    @env.macro
    def include_snippet(file_path: str):
        """Insert ``docs/snippets/<file_path>.yaml`` from the app (path segment lowercased)."""
        return include_yaml(f"docs/snippets/{file_path.lower()}.yaml")

    @env.macro
    def include_crd(crd_plural: str, manifest: str = "manifest.yaml"):
        """DEPRECATED: Use the crd-viewer plugin instead"""
        p = _get_app_file(manifest)
        if not p.exists():
            return f"file does not exist: {p.absolute()}"

        with open(p.absolute()) as f:
            manifest_data = yaml.safe_load(f)

        app_id = manifest_data.get("spec", {}).get("group", "")

        return include_yaml(f"crds/{app_id}_{crd_plural}.yaml")

    @env.macro
    def include_yaml(relative_path: str):
        """Insert the raw text of a file under the app directory (e.g. a YAML spec)."""
        p = _get_app_file(relative_path)
        if not p.exists():
            return f"file does not exist: {p.absolute()}"

        return p.read_text(encoding="utf-8")

    @env.macro
    def ref_app_doc(app_id: str, rel_path: str = "index.md"):
        # Either fully qualified app_id or the app name
        # If plainly using app_name, rel_path will be prefixed with 'resources/' if not empty
        # Examples:
        # ref_app_doc('fabrics', 'isl') # references isl.md page of fabrics app (we prefix with 'resources/')
        # ref_app_doc('fabrics', 'resources/isl') # identical as above
        # ref_app_doc('fabrics.eda.nokia', 'resources/isl') # identical as above, most verbose
        # ref_app_doc('fabrics', '') # references the index.md of fabrics app
        src = Path(env.page.file.abs_src_path)
        if "index.md" in src.parts:
            # index.md sits one level higher than the resources
            base = Path("../")
        else:
            base = Path("../..")

        # add .md suffix if no extension was provided
        if Path(rel_path).suffix == "":
            rel_path += ".md"

        ref_file = (Path(base) / app_id / rel_path).resolve()
        if ref_file.exists():
            return str(ref_file)

        # Not found, input must be an app name instead of app id, parsing manifest to match app name to app id
        docs_dir = Path(env.project_dir) / env.conf.get("extra", {}).get(
            "apps_path", "docs"
        )
        if not docs_dir.exists() or not docs_dir.is_dir():
            # fallback to original/default constructed path
            return str(ref_file)

        for app_docs_dir in docs_dir.iterdir():
            if not app_docs_dir.is_dir():
                continue

            m_file = app_docs_dir / "manifest.yaml"
            if not m_file.exists():
                continue

            with open(m_file) as f:
                manifest_data = yaml.safe_load(f)

            if not manifest_data:
                continue

            app_name = manifest_data.get("metadata", {}).get("name")
            if app_name != app_id:
                continue

            app_id = app_docs_dir.name

            # prefix 'resources' dir if rel_path is not empty
            if rel_path != "index.md" and "resources" not in rel_path:
                rel_path = "resources/" + rel_path
            break

        return str(Path(base) / app_id / rel_path)

    def _get_app_file(rel_path: str) -> Path:
        base = Path(env.page.file.abs_src_path)

        app_path = base.parent
        if base.parent.name == "resources":
            # If the markdown is in the resources directory,
            # we need to go one directory up.
            app_path = app_path.parent

        file = (app_path / rel_path).resolve()
        if file.exists():
            return file
        # check if the file path is relative to 'docs',
        # in that case we should omit the 'docs' directory
        rel = Path(rel_path)
        if not rel.is_relative_to("docs"):
            return file
        return (app_path / (rel.relative_to("docs"))).resolve()


def on_post_page_macros(env):
    """
    Actions to be done after macro interpretation,
    when the macros have been rendered
    """
    if not env.conf.get("extra", {}).get("custom_docs_engine", False):
        return

    output_dir = (Path(env.project_dir) / "output").resolve()

    if not getattr(env.page, "url", None):
        return

    page_url = Path(str(env.page.url))
    if len(page_url.parts) == 0:
        return
    elif len(page_url.parts) == 1:
        # this is the root index markdown, so just replace with 'index' as it should be the index.md file
        page_url = page_url / "docs" / "index"
    else:
        # insert 'docs' directory to keep the output structure aligned to the catalog docs structure
        parts = page_url.parts
        page_url = Path(parts[0], "docs", *parts[1:])

    fp = (output_dir / page_url).resolve()

    parent = fp.parent
    if not parent.exists():
        parent.mkdir(parents=True, exist_ok=True)

    with open(str(fp) + ".md", "w+") as f:
        if hasattr(env, "markdown"):
            f.write(env.markdown)
        elif hasattr(env, "raw_markdown"):
            # backwards compatibility for older versions of the macros plugin;
            # mainly due to the fact that the edabuilder mkdocs image is using the older version.
            f.write(env.raw_markdown)
