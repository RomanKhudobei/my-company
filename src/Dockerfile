FROM python:3.8

COPY ./src /src
COPY requirements.txt /src
RUN pip install -r /src/requirements.txt

RUN pip install gunicorn

EXPOSE 5000
