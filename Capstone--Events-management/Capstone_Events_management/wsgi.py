import os
import sys

# Get the absolute path to the directory *containing* manage.py and the settings module folder
# This correctly sets the base for Django's module resolution.
#just trying out something new. I want to see if this works
path_to_project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Insert the project root path at the beginning of the system path
sys.path.insert(0, path_to_project_root)

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Capstone_Events_management.settings')

application = get_wsgi_application()
