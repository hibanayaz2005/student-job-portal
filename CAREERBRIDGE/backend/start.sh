#!/usr/bin/env bash
# Render start script: runs migrations then starts the server
# Set this as your Render START COMMAND: ./CAREERBRIDGE/backend/start.sh

set -o errexit
cd "$(dirname "$0")"

echo "=== Running database migrations ==="
python manage.py migrate --run-syncdb

echo "=== Starting Daphne server ==="
exec daphne -b 0.0.0.0 -p "${PORT:-8000}" careerbridge.asgi:application
