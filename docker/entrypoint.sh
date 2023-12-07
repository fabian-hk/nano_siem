#!/bin/bash

python3 manage.py migrate # Update database schemes to newest version

python3 -m plugins.http_logs.startup # Execute startup script to initialize and clean up instance

env | grep -v HOME >> /etc/environment
cron # For running background jobs
nginx # Serving static files
gunicorn --timeout 300 -b localhost:8000 -u NanoSiem nano_siem.wsgi