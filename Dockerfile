# syntax=docker/dockerfile:1

FROM python:3.10-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY /api /app/api
RUN mkdir public
COPY public /app/public

#ENV PYTHONPATH "${PYTHONPATH}:/app"
ENV PORT 5000

CMD gunicorn -b 0.0.0.0:$PORT api.index:app