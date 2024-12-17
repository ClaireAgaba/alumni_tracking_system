FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SUPERUSER_USERNAME=admin
ENV DJANGO_SUPERUSER_EMAIL=admin@example.com
ENV DJANGO_SUPERUSER_PASSWORD=adminpassword123
ENV PORT=8000

WORKDIR /code
COPY . /code/

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir -p staticfiles
RUN python manage.py collectstatic --noinput

CMD ["python3","manage.py","runserver","0.0.0.0:8000"]
#CMD gunicorn ubteb_system.wsgi:application --bind 0.0.0.0:$PORT --log-level debug
