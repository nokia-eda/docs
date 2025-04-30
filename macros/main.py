"""
Mkdocs-macros module
"""


def define_env(env):
    """
    Macroses used in SR Linux documentation
    """

    # take eda version from mkdocs.yml .extra.eda_version variable
    # and derive other versions flavors from it
    eda_version = env.variables.eda_version
    eda_v_version = f"v{eda_version}"
    eda_major_version = f"{eda_version.split('.')[0]}"
    eda_minor_version = f"{eda_version.split('.')[1]}"
    eda_major_v_version = f"v{eda_major_version}"
    eda_major_minor_version = f"{eda_major_version}.{eda_minor_version}"
    eda_major_minor_v_version = f"v{eda_major_minor_version}"

    env.variables["eda_v_version"] = eda_v_version
    env.variables["eda_major_minor_version"] = eda_major_minor_version
    env.variables["eda_major_minor_v_version"] = eda_major_minor_v_version
    env.variables["eda_major_version"] = eda_major_version
    env.variables["eda_major_v_version"] = eda_major_v_version

    @env.macro
    def diagram(url, page, title, zoom=2):
        """
        Diagram macro
        """

        # to allow shorthand syntax for drawio URLs, like:
        # srl-labs/srlinux-getting-started/main/diagrams/topology.drawio
        # we will append the missing prefix to it if it doesn't start with http already
        if not url.startswith("http"):
            url = "https://raw.githubusercontent.com/" + url

        diagram_tmpl = f"""
<figure>
    <div class='mxgraph'
            style='max-width:100%;border:1px solid transparent;margin:0 auto; display:block; box-shadow: 0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1); border-radius: 0.25rem;'
            data-mxgraph='{{"url":"{url}","page":{page},"zoom":{zoom},"highlight":"#0000ff","nav":true,"resize":true,"edit":"_blank","dark-mode":false}}'>
    </div>
    {f"<figcaption>{title}</figcaption>" if title else ""}
</figure>
"""

        return diagram_tmpl

    @env.macro
    def video(url):
        """
        HTML5 video macro
        """

        video_tmpl = f"""
<video style="overflow: hidden; box-shadow: 0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1); border-radius: 0.25rem;" width="100%" controls playsinline>
    <source src="{url}" type="video/mp4">
</video>
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
