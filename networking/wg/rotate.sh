#!/usr/bin/env bash
set -euo pipefail

wg genkey | tee privatekey | wg pubkey > publickey
wg set wg0 private-key privatekey
