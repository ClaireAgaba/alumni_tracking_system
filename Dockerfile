FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
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

# Create entrypoint script
RUN echo '#!/bin/bash\n\
python manage.py migrate --noinput\n\
python create_superuser.py\n\
python manage.py collectstatic --noinput\n\
gunicorn ubteb_system.wsgi:application --bind 0.0.0.0:$PORT --workers 4 --timeout 120 --access-logfile -' > /code/entrypoint.sh \
    && chmod +x /code/entrypoint.sh

# Add a health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:$PORT/ || exit 1

# Run the entrypoint script
CMD ["/code/entrypoint.sh"]
