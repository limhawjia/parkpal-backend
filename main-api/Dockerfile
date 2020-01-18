FROM python:3.7.5
ENV FLASK_APP parkpal.py
COPY / /
RUN pip install -r requirements.txt
CMD flask run --host=0.0.0.0
