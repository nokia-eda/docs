from datetime import datetime


def on_config(config, **kwargs):
    current_year = datetime.now().year
    config.copyright = config.copyright.format(current_year=current_year)
