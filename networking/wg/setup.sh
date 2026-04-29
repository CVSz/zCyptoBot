#!/usr/bin/env bash
set -euo pipefail

apt-get update
apt-get install -y wireguard
wg-quick up wg0
