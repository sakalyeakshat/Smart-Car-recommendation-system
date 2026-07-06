#!/bin/sh

echo "Waiting for MySQL..."
sleep 10

echo "Importing cars dataset..."

python database/import_to_mysql.py

if [ $? -ne 0 ]; then
    echo "Database import failed!"
    exit 1
fi

echo "Starting FastAPI..."

exec uvicorn app.main:app --host 0.0.0.0 --port 8000