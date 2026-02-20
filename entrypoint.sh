#!/bin/sh

echo "Waiting for PostgreSQL..."

# Wait until Postgres is ready
while ! nc -z db 5432; do
  sleep 1
done

echo "PostgreSQL started"

echo "Running migrations..."

flask db upgrade

echo "Starting Gunicorn..."

exec gunicorn -w 4 -b 0.0.0.0:8000 run:app