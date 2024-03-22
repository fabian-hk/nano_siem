#!/bin/bash

docker-compose build
docker-compose up -d nano_siem_db
# Wait for database to initialize and load example data
echo "Waiting for database to start..."
sleep 30
docker-compose up -d nano_siem
docker-compose exec nano_siem /bin/bash -c ". ./venv/bin/activate && python manage.py migrate sessions"
docker-compose exec nano_siem /bin/bash -c ". ./venv/bin/activate && python manage.py migrate auth"
docker-compose exec nano_siem /bin/bash -c ". ./venv/bin/activate && python manage.py migrate contenttypes"
docker-compose exec nano_siem /bin/bash -c ". ./venv/bin/activate && python manage.py createsuperuser --username admin --email admin@localhost"
