#!/bin/sh

echo "Waiting for MySQL to be reachable..."

# Poll until MySQL TCP port is open (up to 60 seconds)
MAX_TRIES=30
COUNT=0
until nc -z "${DB_HOST:-db}" "${DB_PORT:-3306}"; do
    COUNT=$((COUNT + 1))
    if [ "$COUNT" -ge "$MAX_TRIES" ]; then
        echo "ERROR: MySQL not reachable after ${MAX_TRIES} attempts. Exiting."
        exit 1
    fi
    echo "  MySQL not ready yet (attempt $COUNT/$MAX_TRIES), retrying in 2s..."
    sleep 2
done

echo "MySQL is up. Starting FastAPI..."

exec uvicorn main:app --host 0.0.0.0 --port 8000 "$@"
