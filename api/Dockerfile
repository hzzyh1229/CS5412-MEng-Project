# syntax=docker/dockerfile:1

FROM python:3.11-slim-buster

EXPOSE 5000

WORKDIR /api

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]