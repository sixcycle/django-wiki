import os
import sys
from django.core.wsgi import get_wsgi_application

sys.path.insert(0, '/opt/python/current/app')
os.environ['DJANGO_SETTINGS_MODULE'] = 'SixcycleWiki.settings'
application = get_wsgi_application()
