#!/usr/bin/env bash
set -euo pipefail

if [ ! -d codeql ]; then
  echo "Downloading CodeQL CLI..."
  curl -fL --retry 3 --retry-all-errors --retry-delay 2 -o codeql.zip \
    https://github.com/github/codeql-cli-binaries/releases/latest/download/codeql.zip
  unzip -tq codeql.zip >/dev/null
  unzip -q codeql.zip -d codeql
  rm codeql.zip
fi

CODEQL=./codeql/codeql/codeql
DB=codeql-db
QUERY_PACK="codeql/python-queries"

# The standalone CLI bundle does not always include query packs.
# Download the Python query pack explicitly so analyze can resolve it.
echo "Ensuring CodeQL query pack is available: ${QUERY_PACK}"
$CODEQL pack download "$QUERY_PACK"

echo "Creating CodeQL database..."
$CODEQL database create "$DB" --overwrite --language=python --source-root=.

echo "Running CodeQL analysis..."
$CODEQL database analyze "$DB" "$QUERY_PACK" \
  --format=sarif-latest --output=codeql-results.sarif

echo "CodeQL analysis complete. Results: codeql-results.sarif"
