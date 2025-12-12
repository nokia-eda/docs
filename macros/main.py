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
    eda_version_dashes = env.variables.eda_version.replace(".", "-")
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
    env.variables["eda_minor_version"] = eda_minor_version
    env.variables["eda_major_v_version"] = eda_major_v_version

    env.variables["eda_version_dashes"] = eda_version_dashes

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
    def video(url, title=""):
        """
        HTML5 video macro
        """

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
    def image(
        url="",
        light_url="",
        dark_url="",
        padding=0,
        border_radius=0.0,
        shadow=False,
        center=True,
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
            title (str): Optional caption/title for the image. Default is "".
        """
        # if shadow is True, apply the .img-shadow class to the image
        if shadow:
            img_class = "img-shadow"
        else:
            img_class = ""

        # if only one url is provided the image is used for both light and dark modes
        img_src = f'<img src="{url}" class="{img_class}" alt="">'

        # if light and dark url are provided
        if light_url and dark_url:
            img_src = f"""
    <img src="{light_url}#only-light" class="{img_class}" alt="">
    <img src="{dark_url}#only-dark" class="{img_class}" alt="">
    """

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
            image_tmpl = f"""
<figure class="polka" style="{figure_style}">
    {img_src}
    <figcaption>{title}</figcaption>
</figure>
"""
        else:
            image_tmpl = f"""
<div class="polka" style="{div_style}">
    {img_src}
</div>
"""

        return image_tmpl
