#!/bin/bash
set -e  # Exit on error

echo "Starting release process..."

# Wait for database to be ready
echo "Waiting for database to be ready..."
for i in {1..30}; do
    if python test_db.py; then
        echo "Database is ready!"
        break
    fi
    if [ $i -eq 30 ]; then
        echo "Database failed to become ready"
        exit 1
    fi
    echo "Waiting for database... attempt $i/30"
    sleep 2
done

echo "Running migrations..."
python manage.py migrate auth
python manage.py migrate sessions
python manage.py migrate admin
python manage.py migrate contenttypes
python manage.py migrate graduates

echo "Creating superuser..."
python create_superuser.py

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Release process completed!"
