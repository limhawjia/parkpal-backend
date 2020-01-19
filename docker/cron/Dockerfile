FROM python:3.7.5

RUN apt-get -y update && apt-get -y upgrade
RUN apt-get install -y cron

ENV PYTHONPATH "/usr/local/lib/python3.7/site-packages"
ENV DB_USER "parkpal"
ENV DB_PASSWORD "secret"
ENV DB_HOST "db"
ENV DB_PORT "5432"
ENV DB_NAME "carparks"

COPY ../../main/ /main
RUN touch hdb_cron.log
RUN touch ura_cron.log
RUN touch lta_cron.log

RUN pip install -r requirements.txt
RUN chmod +x ./startup.py
RUN python -m main.startup

RUN crontab cron
CMD ["cron", "-f"]