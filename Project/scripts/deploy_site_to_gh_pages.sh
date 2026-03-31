#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SITE_DIR="$ROOT_DIR/docs/site"
REPO_URL="$(git -C "$ROOT_DIR" remote get-url origin)"

if [[ ! -d "$SITE_DIR" ]]; then
  echo "docs/site 不存在"
  exit 1
fi

TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

cp -R "$SITE_DIR"/* "$TMP_DIR"/
cd "$TMP_DIR"

git init -q
git checkout -b gh-pages -q
git add .
git -c user.name="site-deploy" -c user.email="site-deploy@example.com" commit -m "Deploy site" -q
git remote add origin "$REPO_URL"
git push -f origin gh-pages

echo "✅ 已推送到 gh-pages 分支"
echo "下一步：GitHub 仓库 Settings -> Pages -> Source 选择 gh-pages / root"
