#!/usr/bin/env bash
set -euo pipefail

if [ ! -d codeql ]; then
  echo "Downloading CodeQL CLI..."
  curl -fL --retry 3 --retry-all-errors --retry-delay 2 -o codeql.zip     https://github.com/github/codeql-cli-binaries/releases/latest/download/codeql-bundle-linux64.zip
  unzip -tq codeql.zip >/dev/null
  unzip -q codeql.zip -d codeql
  rm codeql.zip
fi

CODEQL=./codeql/codeql
DB=codeql-db

echo "Creating CodeQL database..."
$CODEQL database create $DB --language=python --source-root=.

echo "Running CodeQL analysis..."
$CODEQL database analyze $DB --format=sarif-latest --output=codeql-results.sarif

echo "CodeQL analysis complete. Results: codeql-results.sarif"
