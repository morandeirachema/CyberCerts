#!/usr/bin/env bash
# Reset the CEH lab: stop + wipe docker web targets, halt the vagrant VMs.
# Does NOT delete downloaded boxes/images (use the --deep flag for that).
set -euo pipefail

LABS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DEEP="${1:-}"

echo "[*] Stopping and wiping Docker web targets..."
if command -v docker >/dev/null 2>&1; then
  ( cd "$LABS_DIR" && docker compose down -v ) || echo "  (compose not running)"
fi

echo "[*] Halting Vagrant VMs..."
if command -v vagrant >/dev/null 2>&1; then
  ( cd "$LABS_DIR/vagrant" && vagrant halt ) || echo "  (no vagrant VMs)"
fi

if [[ "$DEEP" == "--deep" ]]; then
  echo "[*] Deep clean: destroying VMs and pruning docker volumes..."
  ( cd "$LABS_DIR/vagrant" && vagrant destroy -f ) || true
  docker volume prune -f || true
fi

echo "[+] Lab reset complete."
