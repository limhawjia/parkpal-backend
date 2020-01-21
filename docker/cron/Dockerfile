FROM python:3.7.5

RUN apt-get update || true
RUN apt-get install -y cron

ENV PYTHONPATH "/usr/local/lib/python3.7/site-packages"
ENV DB_USER "parkpal"
ENV DB_PASSWORD "secret"
ENV DB_HOST "db"
ENV DB_PORT "5432"
ENV DB_NAME "carparks"

COPY main/ /main
COPY /scripts/cron /
COPY /scripts/cron_start.sh /
COPY requirements.txt /

RUN touch hdb_cron.log
RUN touch ura_cron.log
RUN touch lta_cron.log

RUN pip install -r requirements.txt
RUN chmod +x ./main/startup.py
RUN chmod +x ./cron_start.sh
RUN crontab cron

CMD ["./cron_start.sh"]