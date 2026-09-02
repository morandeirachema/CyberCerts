#!/usr/bin/env bash
# Assemble the repo's root-level Markdown into a MkDocs docs_dir (./site-src).
# Needed because the content lives at the repo root, while MkDocs 1.6 requires
# docs_dir to be a child directory of mkdocs.yml.
#
# Usage:
#   bash scripts/build-site.sh        # populate ./site-src
#   mkdocs build                      # or: mkdocs serve  /  mkdocs gh-deploy --force
set -euo pipefail
cd "$(dirname "$0")/.."

rm -rf site-src
mkdir -p site-src
# Scripts and workflow files are copied too (as plain static files) so that the
# pages that link to them (README, CONTRIBUTING, MAINTENANCE, certs/ceh/*) resolve
# on the site as well as on GitHub. Issue/PR templates are left out.
rsync -a \
  --exclude '/.git' \
  --include '/.github/' \
  --include '/.github/workflows/***' \
  --exclude '/.github/*' \
  --exclude '.claude' \
  --exclude '/site' \
  --exclude '/site-src' \
  --exclude '/mkdocs.yml' \
  --exclude '__pycache__' \
  ./ site-src/

echo "Populated ./site-src — now run: mkdocs build  (or mkdocs serve / mkdocs gh-deploy --force)"
