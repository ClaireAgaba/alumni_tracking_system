import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ubteb_system.settings')
django.setup()

from graduates.models import User

# Delete existing admin user if exists
User.objects.filter(username='admin').delete()

# Create new admin user with proper user_type
admin = User.objects.create_superuser(
    username='admin',
    email='admin@example.com',
    password='admin123',
)
admin.user_type = 'admin'
admin.save()
