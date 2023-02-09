# Write a New HTTP Log Module

Take a look at the existing [Traefik](../plugins/http_logs/modules/traefik.py) module.
You have to write a method for parsing a single log line and pass it to the
``plugins.http_logs.modules.parse_log_lines`` method. Additionally, you have to
create a ``plugins.http_logs.models.Service`` object and save it to the database.

# Update Models

On model changes run:
- ``export $(cat .env)``
- ``python manage.py makemigrations``
- ``python manage.py migrate``

# Publish Docker Image

- ``docker build -t fabianhk/nano-siem -f docker/Dockerfile .``
- ``docker push fabianhk/nano-siem``