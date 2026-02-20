#!/bin/sh

echo "Waiting for PostgreSQL..."

# Wait for Postgres to be ready
while ! nc -z db 5432; do
  sleep 1
done

echo "PostgreSQL started"

# Check if migrations folder exists
if [ -d "migrations" ]; then

  echo "Migrations folder found"
  echo "Running flask db upgrade..."

  flask db upgrade

else

  echo "No migrations folder found"
  echo "Creating database tables using db.create_all()..."

  flask shell <<EOF
from app import db
db.create_all()
EOF

fi

echo "Starting Gunicorn..."

exec gunicorn -w 4 -b 0.0.0.0:8000 run:app
