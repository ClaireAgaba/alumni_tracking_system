FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SUPERUSER_USERNAME=admin
ENV DJANGO_SUPERUSER_EMAIL=admin@example.com
ENV DJANGO_SUPERUSER_PASSWORD=adminpassword123
ENV PORT=8000

# Set work directory
WORKDIR /code
COPY . /code/

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
        build-essential \
        python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create static directory
RUN python manage.py collectstatic --noinput

# Run gunicorn
CMD python manage.py migrate && python manage.py createsuperuser --noinput || true && gunicorn ubteb_system.wsgi:application --bind 0.0.0.0:$PORT
