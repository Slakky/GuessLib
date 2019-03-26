<<<<<<< HEAD
=======
from __future__ import absolute_import

# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
from .celery import app as celery_app

>>>>>>> f54b90092c6a6fb9f26da8faad07ddf5460a4828
import subprocess

subprocess.run(['chmod', '+x', 'blat'])
