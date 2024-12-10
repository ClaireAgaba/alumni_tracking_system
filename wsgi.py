import os
import sys

# Add your project directory to the sys.path
path = '/home/your_pythonanywhere_username/graduate_tracking_system/alumni_tracking_system'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'ubteb_system.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
