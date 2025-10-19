import os
import sys

# Path fix for Render's nested structure:
# Adds the directory containing 'manage.py' to the Python path.
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '..'))

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Capstone_Events_management.settings')

application = get_wsgi_application()
