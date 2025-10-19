import os
import sys

# FIX: Append the directory containing manage.py (one level up from the settings directory)
sys.path.append(os.path.dirname(os.path.abspath(__file__))) 

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Capstone_Events_management.settings')

application = get_wsgi_application()
