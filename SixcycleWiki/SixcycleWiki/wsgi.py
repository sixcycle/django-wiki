import os
import sys
from django.core.wsgi import get_wsgi_application

sys.path.append("/opt/python/current/app/SixcycleWiki")
os.environ['DJANGO_SETTINGS_MODULE'] = 'SixcycleWiki.settings'
application = get_wsgi_application()
