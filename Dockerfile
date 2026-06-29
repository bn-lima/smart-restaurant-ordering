FROM python:3.12

WORKDIR /app

RUN apt-get update && apt-get install -y netcat-openbsd

COPY requirements.txt .

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["sh", "-c", "until nc -z db 5432; do sleep 1; done; python manage.py migrate && exec gunicorn smart_restaurant.wsgi:application --bind 0.0.0.0:8000 --workers 3 --worker-class gthread --threads 2 --timeout 120 --keep-alive 5"]