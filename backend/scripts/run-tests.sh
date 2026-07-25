#!/bin/sh
set -e

echo "Applying Alembic migrations..."
alembic upgrade head

echo "Running tests..."
pytest
