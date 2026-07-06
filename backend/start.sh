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

echo "MySQL is up. Importing cars dataset..."

# Retry import up to 3 times in case of transient connection issues
IMPORT_TRIES=3
for i in $(seq 1 $IMPORT_TRIES); do
    python database/import_to_mysql.py && break
    echo "Import attempt $i failed, retrying in 3s..."
    sleep 3
    if [ "$i" -eq "$IMPORT_TRIES" ]; then
        echo "WARNING: CSV import failed after $IMPORT_TRIES attempts. Starting API anyway..."
    fi
done

echo "Starting FastAPI..."

exec uvicorn app.main:app --host 0.0.0.0 --port 8000