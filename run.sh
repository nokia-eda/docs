#!/usr/bin/env bash
# Copyright 2024 Nokia
# Licensed under the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause

set -o errexit
set -o pipefail
set -e

# set the host's port via PORT environment variable
# if PORT is not set, default to 8000
if [ -z "${PORT}" ]; then
  PORT=8000
fi

DOCS_ENV=${DOCS_ENV:-internet}

# git remote names
if [ -z "${INSIDERS_REMOTE_NAME}" ]; then
  INSIDERS_REMOTE_NAME="insiders"
fi

if [ -z "${PUBLIC_REMOTE_NAME}" ]; then
  PUBLIC_REMOTE_NAME="public"
fi

# set the branch name for versioned docs
MIKE_BRANCH_NAME="__versioned-docs__"

MKDOCS_VERSION=${MKDOCS_VERSION:-9.6.12-insiders-4.53.16-hellt}

MKDOCS_INET_IMAGE=ghcr.io/nokia-eda/mkdocs-material-insiders:${MKDOCS_VERSION}
MKDOCS_NOKIA_IMAGE=registry.srlinux.dev/pub/mkdocs-material-insiders:${MKDOCS_VERSION}

if [ "${DOCS_ENV}" = "internet" ]; then
  MKDOCS_IMAGE=${MKDOCS_INET_IMAGE}
elif [ "${DOCS_ENV}" = "nokia" ]; then
  echo "Using Nokia internal mkdocs image"
  MKDOCS_IMAGE=${MKDOCS_NOKIA_IMAGE}
else
  echo "Using public mkdocs image"
  MKDOCS_IMAGE=squidfunk/mkdocs-material:9.6.12
fi

MIKE_CMD_COMMON_DOCKER_RUN_ARGS="--rm -i -p ${PORT}:8000 \
  -v $(pwd):/docs \
  -v ${HOME}/.ssh:/root/.ssh \
  --user $(id -u):$(id -g) \
  --env GIT_COMMITTER_NAME=nokia-eda-bot --env GIT_COMMITTER_EMAIL=nokia-eda-bot@eda.nokia.com \
  --entrypoint mike"

if [ "${CI}" = "true" ]; then
  MIKE_CMD="docker run ${MIKE_CMD_COMMON_DOCKER_RUN_ARGS} \
  --env GIT_COMMITTERS=true \
  --env MKDOCS_GIT_COMMITTERS_APIKEY=${GITHUB_TOKEN} \
  ${MKDOCS_IMAGE}"

  MIKE_BRANCH_NAME="__versioned-docs__"
else
  MIKE_CMD="docker run -t ${MIKE_CMD_COMMON_DOCKER_RUN_ARGS} \
  -v $(echo $SSH_AUTH_SOCK):/tmp/ssh_agent_socket \
  -e SSH_AUTH_SOCK=/tmp/ssh_agent_socket \
  --user $(id -u):$(id -g) \
  ${MKDOCS_IMAGE}"

  MIKE_BRANCH_NAME="local__versioned-docs__"
fi

function serve-docs {
  # serve development documentation portal
  docker run -it --rm -p ${PORT}:8000 -v "$(pwd)":/docs ${MKDOCS_IMAGE} serve --dirtyreload -a 0.0.0.0:8000
}

function serve-docs-full {
  # serve development documentation portal
  docker run -it --rm -p ${PORT}:8000 -v "$(pwd)":/docs ${MKDOCS_IMAGE} serve -a 0.0.0.0:8000
}

function build-docs {
  docker run --rm -v "$(pwd)":/docs --entrypoint mkdocs ${MKDOCS_IMAGE} build --clean # --strict
}

function test-docs {
	build-docs
  # docker build produces root:root ownership. Claim it back for seds sake
  sudo chown -R $USER:$USER ./site
  # replace empty href patterns that are result of version picker script not being templated
  # properly since we are not building with `mike` here. We replace these links with #
  # as they are not important for link testing
  find ./site -type f -name "*.html" -exec sed -i 's|href=\.\./[\.\/ ]*>|href="#">|g' {} +

  docker run --rm -u $(id -u):$(id -g) -v "$(pwd)":/test wjdp/htmltest --conf ./site/htmltest.yml

	sudo rm -rf ./site
}

# -----------------------------------------------------------------------------
# Version management.
# -----------------------------------------------------------------------------

function list-versions {
  ${MIKE_CMD} list -b ${MIKE_BRANCH_NAME}
}

# build-version builds a current version and names it according to passed argument(s).
# example usage:
# build-version 25.4 latest
# this operation does not push the changes to the remote and only modifies the local repository.
function build-version {
  # if ./site or ./.cache exist, chown them as they may be owned by root
  # as a result of containerized builds
  [ -d ./site ] && sudo chown -R $USER:$USER ./site
  [ -d ./.cache ] && sudo chown -R $USER:$USER ./.cache
  ${MIKE_CMD} deploy -b ${MIKE_BRANCH_NAME} --update-aliases "$@"

  # copy the 404 page to the root of the site
  # see https://github.com/jimporter/mike/issues/248
  CUR_BRANCH=$(git branch --show-current)
  git config --global user.email "nokia-eda-bot@eda.nokia.com"
  git config --global user.name "nokia-eda-bot"
  git checkout ${MIKE_BRANCH_NAME}
  cp $1/404.html 404.html
  git add 404.html
  git diff --cached --quiet || git commit -m "Copy 404 page to root for version $1"
  git checkout ${CUR_BRANCH}
}

# set the default version in the __versioned-docs__ branch to the specified version.
function set-default-version {
  ${MIKE_CMD} set-default -b ${MIKE_BRANCH_NAME} --allow-empty "$@"
}

# serve the versioned docs from the __versioned-docs__ branch from a remote repository.
function serve-versioned-docs {
  ${MIKE_CMD} serve -a 0.0.0.0:8000 -b ${MIKE_BRANCH_NAME}
}

# delete a version or an alias from the versioned docs.
function mike-delete {
  ${MIKE_CMD} delete -b ${MIKE_BRANCH_NAME} $@
}

# add an alias to a version.
# example usage:
# mike-alias 25.4 latest
function mike-alias {
  ${MIKE_CMD} alias -b ${MIKE_BRANCH_NAME} $@
}

function mike-shell {
  MIKE_CMD="docker run -it --rm -p ${PORT}:8000 \
  -v $(pwd):/docs \
  -v ${HOME}/.gitconfig:/root/.gitconfig \
  -v ${HOME}/.ssh:/root/.ssh \
  -v $(echo $SSH_AUTH_SOCK):/tmp/ssh_agent_socket \
  -e SSH_AUTH_SOCK=/tmp/ssh_agent_socket \
  --entrypoint ash ${MKDOCS_IMAGE}"

  ${MIKE_CMD}
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
