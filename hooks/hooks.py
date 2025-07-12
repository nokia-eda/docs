from datetime import datetime


def on_config(config, **kwargs):
    # set current_year in the copyright
    current_year = datetime.now().year
    config.copyright = config.copyright.format(current_year=current_year)

    # set the versioned docs branch
    eda_version = config.extra["eda_version"]
    eda_major_version = f"{eda_version.split('.')[0]}"
    eda_minor_version = f"{eda_version.split('.')[1]}"
    eda_major_minor_version = f"{eda_major_version}.{eda_minor_version}"
    config.edit_uri = config.edit_uri.format(versioned_branch="release-"+eda_major_minor_version)
