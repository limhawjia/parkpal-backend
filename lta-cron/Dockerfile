FROM python:3.7.5
RUN apt-get -y update && apt-get -y upgrade
RUN apt-get install -y cron
RUN touch /var/log/cron.log
COPY / /
RUN pip install -r requirements.txt
RUN crontab lta-cron
CMD ["cron", "-f"]
