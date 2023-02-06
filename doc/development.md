# Update Models

On model changes run:
- ``export $(cat .env)``
- ``python manage.py makemigrations``
- ``python manage.py migrate``