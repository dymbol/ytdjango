from __future__ import absolute_import

import os

from celery import Celery
from website import extras

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ytdjango.settings')

from django.conf import settings

app = Celery('proj')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


@app.task(bind=True)
def download(self, YT_url_object, url, user):
    extras.download_yt_mp3(YT_url_object, url, user)