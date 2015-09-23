import os
import sys
sys.path.append('/media/GIT-private/gogs/ytdjango/ytdjango')
os.environ['DJANGO_SETTINGS_MODULE'] = 'ytdjango.settings'
#import django.core.handlers.wsgi
#application = django.core.handlers.wsgi.WSGIHandler()

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
