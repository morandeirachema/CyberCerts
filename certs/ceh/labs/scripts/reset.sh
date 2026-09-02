#!/usr/bin/env bash
# Reset the CEH lab: stop + wipe docker web targets, halt the vagrant VMs.
# Does NOT delete downloaded boxes/images (use the --deep flag for that).
set -euo pipefail

LABS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DEEP="${1:-}"

echo "[*] Stopping and wiping Docker web + OT targets..."
if command -v docker >/dev/null 2>&1; then
  ( cd "$LABS_DIR" && docker compose down -v ) || echo "  (web compose not running)"
  ( cd "$LABS_DIR/ot" && docker compose down -v ) || echo "  (ot compose not running)"
fi

echo "[*] Halting Vagrant VMs..."
if command -v vagrant >/dev/null 2>&1; then
  ( cd "$LABS_DIR/vagrant" && vagrant halt ) || echo "  (no vagrant VMs)"
fi

if [[ "$DEEP" == "--deep" ]]; then
  echo "[*] Deep clean: destroying VMs and removing THIS lab's images..."
  ( cd "$LABS_DIR/vagrant" && vagrant destroy -f ) || true
  # Scope removal to these compose projects only. A global 'docker volume prune'
  # would delete unrelated dangling volumes elsewhere on the host — never do that.
  ( cd "$LABS_DIR" && docker compose down -v --rmi all --remove-orphans ) || true
  ( cd "$LABS_DIR/ot" && docker compose down -v --rmi all --remove-orphans ) || true
fi

echo "[+] Lab reset complete."
