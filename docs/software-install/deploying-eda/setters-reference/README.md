# Generating KPT setters reference documentation

To generate the setters reference documentation, go to the playground directory, ensure that packages are downloaded for the right version, and run:

```bash
uv run scripts/list-setters.py --markdown eda-kpt/eda-kpt-base
```

```bash
uv run scripts/list-setters.py --markdown eda-kpt/eda-external-packages
```

```bash
uv run scripts/list-setters.py --markdown ./eda-kpt/eda-kpt-playground
```
