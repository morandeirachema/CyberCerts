#!/usr/bin/env bash
# Preflight + bring up the Docker web-target range.
# Vagrant + Ansible layers are brought up separately (see labs/README.md).
set -euo pipefail

LABS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$LABS_DIR"

echo "[*] Preflight checks..."
missing=0
for bin in docker; do
  if ! command -v "$bin" >/dev/null 2>&1; then
    echo "  ✗ $bin not found — see labs/README.md prerequisites"; missing=1
  fi
done
if ! docker compose version >/dev/null 2>&1; then
  echo "  ✗ 'docker compose' v2 not available"; missing=1
fi
[[ "$missing" -eq 1 ]] && { echo "[!] Install missing prerequisites first."; exit 1; }

[[ -f .env ]] || { echo "[*] Creating .env from example..."; cp .env.example .env; }

echo "[*] Pulling and starting web targets (bound to 127.0.0.1)..."
docker compose up -d

echo "[*] Status:"
docker compose ps

cat <<'EOF'

[+] Web targets up (localhost only):
    DVWA        http://localhost:8081   (admin / password)
    Juice Shop  http://localhost:8082   (self-register)
    WebGoat     http://localhost:8083/WebGoat
    bWAPP       http://localhost:8084   (visit /install.php first, then bee/bug)

Next: cd vagrant && vagrant up      (network targets)
      see ansible/README.md         (AD / PAM lab)
EOF
