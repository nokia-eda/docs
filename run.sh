#!/usr/bin/env bash
# Copyright 2024 Nokia
# Licensed under the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause

set -o errexit
set -o pipefail
set -e

PORT=${2:-8000}

MKDOCS_IMAGE=ghcr.io/nokia-eda/mkdocs-material-insiders:9.6.12-insiders-4.53.16-hellt

MIKE_CMD="docker run -it --rm -p ${PORT}:8000 \
-v $(pwd):/docs \
-v ${HOME}/.gitconfig:/root/.gitconfig \
-v ${HOME}/.ssh:/root/.ssh \
-v $(echo $SSH_AUTH_SOCK):/tmp/ssh_agent_socket \
-e SSH_AUTH_SOCK=/tmp/ssh_agent_socket \
--entrypoint mike ${MKDOCS_IMAGE}"

function serve-docs {
  # serve development documentation portal
  docker run -it --rm -p ${PORT}:8000 -v $(pwd):/docs ${MKDOCS_IMAGE} serve --dirtyreload -a 0.0.0.0:8000
}

function serve-docs-full {
  # serve development documentation portal
  docker run -it --rm -p ${PORT}:8000 -v $(pwd):/docs ${MKDOCS_IMAGE} serve -a 0.0.0.0:8000
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
# Version management.
# -----------------------------------------------------------------------------

function list-versions {
  ${MIKE_CMD} list -r internal -b versioned-docs-test
}

function build-versions {
  ${MIKE_CMD} deploy $1
}

function set-default-version {
  ${MIKE_CMD} set-default -r internal -b versioned-docs-test --push latest
}

function deploy-version {
  ${MIKE_CMD} deploy -r internal -b versioned-docs-test --push $@
}

function mike-serve {
  ${MIKE_CMD} serve -a 0.0.0.0:8000 -r internal -b versioned-docs-test
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
