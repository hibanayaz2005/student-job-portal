#!/usr/bin/env bash
# Exit on error
set -o errexit

# Move to the script's own directory so all paths are relative to it
cd "$(dirname "$0")"

echo "=== Installing dependencies ==="
pip install -r ../../requirements.txt

echo "=== Collecting static files ==="
# Use || true so a collectstatic warning/error doesn't abort the build
python manage.py collectstatic --no-input || echo "WARNING: collectstatic had issues, continuing..."

echo "=== Running database migrations ==="
python manage.py migrate

echo "=== Build complete ==="
