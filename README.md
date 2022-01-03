## Online service for generating CSV-files with fake (dummy) data

python manage.py runserver (to run the web project)

STEP 2

docker-compose up -d (to run the redis)

STEP 3

celery -A generation_system worker -l info --pool=solo (to run celery)
