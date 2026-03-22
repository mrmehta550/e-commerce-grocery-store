
import sys
import os

path = '/home/mrmehta5500/freshshop'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'freshshop.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()