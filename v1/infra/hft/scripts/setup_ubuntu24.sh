#!/usr/bin/env bash
set -euo pipefail

sudo apt update
sudo apt install -y \
  bpfcc-tools \
  linux-headers-"$(uname -r)" \
  dpdk \
  dpdk-dev \
  linuxptp \
  ethtool

echo "Example tuning commands (review before applying in prod):"
echo "  sudo ethtool -K eth0 gro off gso off tso off"
echo "  sudo ethtool -C eth0 rx-usecs 0"
echo "  echo 1024 | sudo tee /proc/sys/vm/nr_hugepages"
