#!/usr/bin/env bash
set -euo pipefail

for i in {1..5}; do
  k6 run --out json="out_${i}.json" script.js &
done
wait
