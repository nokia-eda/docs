from datetime import datetime


def on_config(config, **kwargs):
    config.copyright = f"Copyright © 2023-{datetime.now().year} Nokia"
