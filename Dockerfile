FROM python:3.8.2

ENV PYTHONUNBUFFERRED 1
ENV PORT 8000

EXPOSE 8000

RUN mkdir /app

WORKDIR /app

COPY requirements.txt /app

RUN pip install -r requirements.txt

COPY . /app/
