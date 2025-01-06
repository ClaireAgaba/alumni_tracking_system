#!/bin/bash
set -e  # Exit on error

echo "Starting release process..."

echo "Testing database connection..."
python test_db.py

echo "Removing any existing migrations..."
rm -f graduates/migrations/0*.py
python manage.py makemigrations graduates

echo "Showing current migration status..."
python manage.py showmigrations graduates

echo "Running migrations..."
python manage.py migrate --no-input

echo "Creating superuser..."
python create_superuser.py

echo "Verifying database setup..."
python test_db.py

echo "Release process completed!"
