import os
from celery import Celery
from celery import shared_task

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'generation_system.settings')
# os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')

app = Celery('generation_system')
app.config_from_object('django.conf:settings',namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

@shared_task(bind=True)
def add(x, y):
    print(x + y)
    return x + y
