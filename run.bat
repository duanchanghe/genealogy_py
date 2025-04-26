python -m pip install -r requirements.txt
python manage.py createsuperuser
python manage.py migrate
python manage.py makemigrations
python manage.py runserver
