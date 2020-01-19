FROM python:3.7.5
ENV FLASK_APP "parkpal.py"
ENV DB_USER "ParkPal"
ENV DB_PASSWORD "ParkPal"
ENV DB_HOST "db"
ENV DB_PORT "5432"
ENV DB_NAME "parking_lots"

COPY ./main/ /main
COPY requirements.txt /

RUN pip install -r requirements.txt
RUN cd main
CMD ["flask", "run", "--host=0.0.0.0"]
