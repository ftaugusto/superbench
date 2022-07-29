FROM python:3.9-slim-bullseye

COPY requirements.txt /
RUN pip3 install -r /requirements.txt
COPY . /app
WORKDIR /app

CMD ["gunicorn"  , "-b", "0.0.0.0:8000", "superbench:server"]
