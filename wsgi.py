import os, sys
sys.path.append('/sites/regis')
os.environ['DJANGO_SETTINGS_MODULE'] = 'face.settings'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()
