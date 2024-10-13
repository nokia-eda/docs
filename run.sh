#!/usr/bin/env bash
# Copyright 2024 Nokia
# Licensed under the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause


set -o errexit
set -o pipefail
set -e

MKDOCS_IMAGE=ghcr.io/nokia-eda/mkdocs-material-insiders:9.5.35-insiders-4.53.13-hellt

function serve-docs {
  # serve development documentation portal
  docker run -it --rm -p 8000:8000 -v $(pwd):/docs ${MKDOCS_IMAGE} serve --dirtyreload -a 0.0.0.0:8000
}

function serve-docs-full {
  # serve development documentation portal
  docker run -it --rm -p 8000:8000 -v $(pwd):/docs ${MKDOCS_IMAGE} serve -a 0.0.0.0:8000
}

function build-docs {
  docker run --rm -v $(pwd):/docs --entrypoint mkdocs ${MKDOCS_IMAGE} build --clean --strict
}

function test-docs {
	docker run --rm -v $(pwd):/docs --entrypoint mkdocs ${MKDOCS_IMAGE} build --clean --strict
	docker run --rm -v $(pwd):/test wjdp/htmltest --conf ./site/htmltest.yml
	sudo rm -rf ./site
}

# -----------------------------------------------------------------------------
# Bash runner functions.
# -----------------------------------------------------------------------------
function help {
  printf "%s <task> [args]\n\nTasks:\n" "${0}"

  compgen -A function | grep -v "^_" | cat -n

  printf "\nExtended help:\n  Each task has comments for general usage\n"
}

# This idea is heavily inspired by: https://github.com/adriancooney/Taskfile
TIMEFORMAT=$'\nTask completed in %3lR'
time "${@:-help}"