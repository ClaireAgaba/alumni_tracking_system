import os
import sys
import django
from django.db import connections
from django.db.utils import OperationalError
import MySQLdb

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ubteb_system.settings')
django.setup()

def test_connection():
    try:
        # First try raw MySQL connection
        print("Testing raw MySQL connection...")
        conn = MySQLdb.connect(
            host='monorail.proxy.rlwy.net',
            port=21891,
            user='root',
            password='dFbcF3H6e4Hf2-5EEFhfGGBECFhB5hc6',
            db='railway'
        )
        print("Raw MySQL connection successful!")
        
        # Now test Django connection
        print("\nTesting Django database connection...")
        db_conn = connections['default']
        c = db_conn.cursor()
        print("Django database connection successful!")
        
        # Test if tables exist
        print("\nChecking existing tables...")
        c.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'railway'
        """)
        tables = c.fetchall()
        if tables:
            print("Found tables:")
            for table in tables:
                print(f"- {table[0]}")
        else:
            print("No tables found in database")
            
        return True
            
    except MySQLdb.Error as e:
        print(f"MySQL connection failed: {e}", file=sys.stderr)
        return False
    except OperationalError as e:
        print(f"Django database connection failed: {e}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)
        return False

if __name__ == "__main__":
    success = test_connection()
    sys.exit(0 if success else 1)
