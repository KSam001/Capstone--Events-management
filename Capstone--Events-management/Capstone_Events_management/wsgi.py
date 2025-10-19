import os
import sys
from pathlib import Path

# Get the path to the inner directory (where wsgi.py is)
SETTINGS_DIR = Path(__file__).resolve().parent

# Get the path to the top-level project directory (containing manage.py)
# This assumes wsgi.py is inside a folder, which is inside the project root
PROJECT_ROOT_DIR = SETTINGS_DIR.parent

# Add the project root to the system path to enable module imports
sys.path.insert(0, str(PROJECT_ROOT_DIR))

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Capstone_Events_management.settings')

application = get_wsgi_application()
