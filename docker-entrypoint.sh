#!/bin/bash

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL..."
while ! nc -z postgres 5432; do
  sleep 0.1
done
echo "PostgreSQL started"

cd /EosGround/postgresDB

# Run migrations
python3 manage.py makemigrations
python3 manage.py migrate

# Keep container running
# tail -f /dev/null

python3 manage.py runserver 0.0.0.0:8000
