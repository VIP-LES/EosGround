#!/bin/bash

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL..."
while ! nc -z postgres 5432; do
  sleep 0.1
done
echo "PostgreSQL started"
echo "Pipeline starting..."

cd /EosGround




# Keep container running
# tail -f /dev/null

PYTHONPATH="/EosGround"
export PYTHONPATH

python3 -u EosGround/database/pipeline
