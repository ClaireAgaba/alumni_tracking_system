#!/bin/bash
set -e  # Exit on error

echo "Starting release process..."

echo "Making migrations..."
python manage.py makemigrations graduates

echo "Showing current migration status..."
python manage.py showmigrations graduates

echo "Running migrations..."
python manage.py migrate

echo "Creating superuser..."
python create_superuser.py

echo "Release process completed!"
