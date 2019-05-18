FROM python:3.5

ENV PYTHONUNBUFFERED=1
RUN mkdir /django
COPY . /django/
WORKDIR /django
RUN pip install -r requirements.txt
RUN pip install psycopg2 --quiet
