## Online service for generating CSV-files with fake (dummy) data

## Run  
Install requirements for this project
```
pip install -r requirementa.txt
```
Navigate to the project directory (where manage.py is located) and run
```
python manage.py makemigrations
python manage.py migrate
```
Create superuser for django admin panel
```
python manage.py createsuperuser
```
Run the project
```
python manage.py runserver
```
Run the redis for celery

```
docker-compose up -d
``` 

Run celery

```
celery -A generation_system worker -l info --pool=solo
```

After running the above command, the survey application will be available at http://localhost:8000/survey 

The admin portal can be accessed at http://localhost:8000/admin
python manage.py runserver (to run the web project)




