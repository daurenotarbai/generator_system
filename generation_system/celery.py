import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'generation_system.settings')
# os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')

app = Celery('generation_system')
app.config_from_object('django.conf:settings',namespace='CELERY')

# app.conf.update(BROKER_URL=os.environ['REDIS_URL'],
#                 CELERY_RESULT_BACKEND=os.environ['REDIS_URL'])

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
