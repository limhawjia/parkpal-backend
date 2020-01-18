FROM python:3.7.5
RUN apt-get -y update && apt-get -y upgrade
RUN apt-get install -y cron
ENV PYTHONPATH "/usr/local/lib/python3.7/site-packages"
ENV DB_USER "parkpal"
ENV DB_PASSWORD "secret"
ENV DB_HOST "db"
ENV DB_PORT "5432"
ENV DB_NAME "carparks"
COPY /cron /cron
COPY /database /cron/database
WORKDIR /cron
RUN touch cron.log
RUN pip install -r requirements.txt
RUN chmod +x ./cron.py
RUN crontab cron
CMD ["cron", "-f"]