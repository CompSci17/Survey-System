"""
WSGI config for survey_system project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "survey_system.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

import survey_system.monitor
survey_system.monitor.start(interval=1.0)