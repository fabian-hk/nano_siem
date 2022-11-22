FROM python:3.11.0-buster

WORKDIR /var/nano_siem

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY configure .
RUN ./configure

RUN useradd -ms /bin/bash -u 1000 NanoSiem
USER NanoSiem

COPY . .

RUN python manage.py crontab add

USER root
CMD env >> /etc/environment && cron && gunicorn -b 0.0.0.0:8000 -u NanoSiem nano_siem.wsgi