import os
import django
import sys

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ubteb_system.settings')
django.setup()

from django.db import connections
from django.db.utils import OperationalError
from graduates.models import Graduate, Course, District, ExamCenter
from django.contrib.auth import get_user_model

def test_connection():
    print("Testing database connection...")
    
    try:
        # Test raw database connection
        db_conn = connections['default']
        db_conn.cursor()
        print("✓ Database connection successful!")
        
        # Test model queries
        User = get_user_model()
        print("\nCounting records:")
        print(f"✓ Users: {User.objects.count()}")
        print(f"✓ Graduates: {Graduate.objects.count()}")
        print(f"✓ Courses: {Course.objects.count()}")
        print(f"✓ Districts: {District.objects.count()}")
        print(f"✓ Exam Centers: {ExamCenter.objects.count()}")
        
        # Test database configuration
        from django.conf import settings
        db_settings = settings.DATABASES['default']
        print("\nDatabase Configuration:")
        print(f"✓ Engine: {db_settings['ENGINE']}")
        print(f"✓ Name: {db_settings['NAME']}")
        print(f"✓ Host: {db_settings['HOST']}")
        print(f"✓ Port: {db_settings['PORT']}")
        
        return True
        
    except OperationalError as e:
        print(f"ERROR: Could not connect to database: {e}")
        return False
    except Exception as e:
        print(f"ERROR: An unexpected error occurred: {e}")
        return False

if __name__ == "__main__":
    success = test_connection()
    sys.exit(0 if success else 1)
