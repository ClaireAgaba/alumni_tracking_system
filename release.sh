#!/bin/bash
set -e  # Exit on error

echo "Starting release process..."

echo "Waiting for MySQL to be ready..."
python - << END
import sys
import time
import MySQLdb

for i in range(30):
    try:
        MySQLdb.connect(
            host='monorail.proxy.rlwy.net',
            port=21891,
            user='root',
            password='dFbcF3H6e4Hf2-5EEFhfGGBECFhB5hc6',
            db='railway'
        )
        print("MySQL is ready!")
        sys.exit(0)
    except MySQLdb.Error as e:
        print(f"MySQL not ready yet (attempt {i+1}/30): {e}")
        time.sleep(1)
sys.exit(1)
END

echo "Making migrations..."
python manage.py makemigrations graduates

echo "Showing current migration status..."
python manage.py showmigrations graduates

echo "Running migrations..."
python manage.py migrate

echo "Creating superuser..."
python create_superuser.py

echo "Release process completed!"
