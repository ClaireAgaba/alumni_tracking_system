import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ubteb_system.settings')
django.setup()

from django.contrib.auth import get_user_model
from graduates.models import User

def create_superuser():
    try:
        superuser = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123',
            first_name='Admin',
            last_name='User',
            user_type='admin'
        )
        print("Superuser created successfully!")
        return superuser
    except Exception as e:
        print(f"Error creating superuser: {e}")

if __name__ == "__main__":
    create_superuser()
