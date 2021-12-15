FROM python:3.9.7

WORKDIR /code
COPY requirements.txt .
RUN pip3 install -U pip && pip3 install -r requirements.txt
COPY . .
CMD gunicorn backend.wsgi:application --bind 0.0.0.0:8000