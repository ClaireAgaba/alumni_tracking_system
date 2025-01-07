"""
WSGI config for ubteb_system project.
"""

import os
import sys
import logging
from django.core.wsgi import get_wsgi_application

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

try:
    logger.info("Initializing WSGI application...")
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ubteb_system.settings')
    application = get_wsgi_application()
    logger.info("WSGI application initialized successfully")
except Exception as e:
    logger.error(f"Error initializing WSGI application: {str(e)}")
    raise
