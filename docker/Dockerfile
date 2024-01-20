FROM ubuntu:24.04

WORKDIR /var/nano_siem

COPY configure .
RUN ./configure

COPY requirements.txt .
RUN python3 -m venv venv
RUN . venv/bin/activate && pip install -r requirements.txt

USER ubuntu

COPY . .

RUN . venv/bin/activate && python manage.py crontab add

RUN mkdir /home/ubuntu/.nano_siem
RUN mkdir /home/ubuntu/.nano_siem/geolite2

USER root

RUN . venv/bin/activate && python manage.py collectstatic
COPY docker/nginx.conf /etc/nginx/nginx.conf
COPY docker/mime.types /etc/nginx/conf/mime.types

RUN echo "@reboot ubuntu /usr/bin/geoipupdate -v -d /home/ubuntu/.nano_siem/geolite2 >> /home/ubuntu/.nano_siem/crontab.log 2>&1" >> /etc/crontab
RUN echo "58 5 * * 6,3 ubuntu /usr/bin/geoipupdate -v -d /home/ubuntu/.nano_siem/geolite2 >> /home/ubuntu/.nano_siem/crontab.log 2>&1" >> /etc/crontab

COPY docker/entrypoint.sh .
RUN chmod +x entrypoint.sh

CMD /var/nano_siem/entrypoint.sh