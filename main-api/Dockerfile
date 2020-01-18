FROM python:3.7.5
ENV FLASK_APP parkpal.py
ENV DB_USER "ParkPal"
ENV DB_PASSWORD "ParkPal"
ENV DB_HOST "db"
ENV DB_PORT "5432"
ENV DB_NAME "parking_lots"
COPY /main-api /main-api
COPY /database /main-api/database
WORKDIR /main-api
RUN pip install -r requirements.txt
CMD flask run --host=0.0.0.0
