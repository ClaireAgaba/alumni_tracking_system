import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ubteb_system.settings')
django.setup()

from graduates.models import User

def create_superuser():
    print("Attempting to create superuser...", file=sys.stderr)
    try:
        if User.objects.filter(username='admin').exists():
            print("Superuser 'admin' already exists.", file=sys.stderr)
            admin = User.objects.get(username='admin')
            admin.user_type = 'admin'
            admin.save()
            print("Updated admin user_type.", file=sys.stderr)
        else:
            User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='12345',
                user_type='admin'
            )
            print("Superuser created successfully!", file=sys.stderr)
        return True
    except Exception as e:
        print(f"Error creating superuser: {str(e)}", file=sys.stderr)
        return False

if __name__ == "__main__":
    success = create_superuser()
    sys.exit(0 if success else 1)
