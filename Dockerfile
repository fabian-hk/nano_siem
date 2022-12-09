FROM ubuntu:22.04

WORKDIR /var/nano_siem

COPY configure .
RUN ./configure

COPY requirements.txt .
RUN pip3 install -r requirements.txt

RUN useradd -ms /bin/bash -u 1000 NanoSiem

USER NanoSiem

COPY . .

RUN python3 manage.py crontab add

RUN mkdir /home/NanoSiem/.nano_siem
RUN mkdir /home/NanoSiem/.nano_siem/geolite2

USER root

RUN echo "@reboot NanoSiem /usr/bin/geoipupdate -v -d /home/NanoSiem/.nano_siem/geolite2 >> /home/NanoSiem/.nano_siem/crontab.log 2>&1" >> /etc/crontab
RUN echo "58 5 * * 6,3 NanoSiem /usr/bin/geoipupdate -v -d /home/NanoSiem/.nano_siem/geolite2 >> /home/NanoSiem/.nano_siem/crontab.log 2>&1" >> /etc/crontab

CMD env >> /etc/environment && cron && gunicorn --timeout 300 -b 0.0.0.0:8000 -u NanoSiem nano_siem.wsgi