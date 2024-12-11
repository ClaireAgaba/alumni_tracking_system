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
        curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create necessary directories
RUN mkdir -p staticfiles static

# Collect static files
RUN python manage.py collectstatic --noinput

# Add a health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:$PORT/ || exit 1

# Run migrations and start server
CMD python manage.py migrate && \
    python manage.py createsuperuser --noinput || true && \
    gunicorn ubteb_system.wsgi:application --bind 0.0.0.0:$PORT --workers 4 --timeout 120 --access-logfile -
