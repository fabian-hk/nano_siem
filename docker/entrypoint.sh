#!/bin/bash

. venv/bin/activate

python manage.py migrate # Update database schemes to newest version

python -m plugins.http_logs.startup # Execute startup script to initialize and clean up instance

env | grep -v HOME >> /etc/environment
cron # For running background jobs
nginx # Serving static files
gunicorn --timeout 300 -b localhost:8000 -u ubuntu nano_siem.wsgi