import os
import sys
import django
from django.db import connections
from django.db.utils import OperationalError

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ubteb_system.settings')
django.setup()

def test_connection():
    print("Testing database connection...")
    try:
        db_conn = connections['default']
        c = db_conn.cursor()
        print("Successfully connected to database!")
        
        # Test if tables exist
        c.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'railway'
        """)
        tables = c.fetchall()
        print("\nExisting tables:")
        for table in tables:
            print(f"- {table[0]}")
            
    except OperationalError as e:
        print(f"Database connection failed: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    test_connection()
