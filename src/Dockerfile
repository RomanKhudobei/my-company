FROM python:3.8

ENV PYTHONUNBUFFERED 1

WORKDIR /my-company

COPY ./src ./src
COPY ./tests ./tests
COPY ./migrations ./migrations
COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ENV FLASK_APP="src.wsgi:app"
ENV FLASK_ENV=development
ENV PYTHONPATH="/my-company/src:${PYTHONPATH}"

RUN pip install gunicorn
