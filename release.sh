#!/bin/bash
set -e  # Exit on error

echo "Starting release process..."

echo "Checking environment..."
if [ -z "$DATABASE_URL" ]; then
    echo "ERROR: DATABASE_URL is not set!"
    exit 1
fi

echo "Running migrations..."
python manage.py showmigrations
python manage.py migrate --noinput

echo "Creating superuser..."
python create_superuser.py

echo "Release process completed!"
