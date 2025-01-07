import os
import django
from django.contrib.auth import get_user_model

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ubteb_system.settings')
django.setup()

User = get_user_model()

def setup_dev_environment():
    # Create admin user if it doesn't exist
    if not User.objects.filter(username='admin').exists():
        admin = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123'
        )
        admin.user_type = 'admin'
        admin.save()
        print("Created admin user")
    
    # Add any other development setup steps here
    # For example:
    # - Create test data
    # - Set up initial configurations
    
if __name__ == "__main__":
    setup_dev_environment()
