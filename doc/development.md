# Start Development Server

- Set environment variable: ``DEBUG=True``
- Execute ``python manage.py runserver``

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

```bash
docker buildx build --push --platform linux/amd64 -t fabianhk/nano-siem:amd64-latest -f docker/Dockerfile .
docker buildx build --push --platform linux/arm64 -t fabianhk/nano-siem:arm64-latest -f docker/Dockerfile .
docker manifest create fabianhk/nano-siem fabianhk/nano-siem:amd64-latest fabianhk/nano-siem:arm64-latest
docker manifest push fabianhk/nano-siem
```