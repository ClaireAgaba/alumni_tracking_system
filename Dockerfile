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
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install -r requirements.txt

# Create static directory
RUN python manage.py collectstatic --noinput

# Run gunicorn
CMD python manage.py migrate && gunicorn ubteb_system.wsgi:application --bind 0.0.0.0:$PORT
