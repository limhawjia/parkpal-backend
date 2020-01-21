FROM python:3.7.5

ENV FLASK_APP "parkpal.py"
ENV DB_USER "parkpal"
ENV DB_PASSWORD "secret"
ENV DB_HOST "db"
ENV DB_PORT "5432"
ENV DB_NAME "carparks"

COPY requirements.txt /
RUN pip install -r requirements.txt

COPY ./main/ /main

WORKDIR /main
CMD ["flask", "run", "--host=0.0.0.0"]
