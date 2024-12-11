FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PORT 8000

# Create and switch to a non-root user
RUN useradd -m -s /bin/bash appuser

# Set work directory and change ownership
WORKDIR /app
RUN chown appuser:appuser /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
        build-essential \
        python3-dev \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Switch to non-root user
USER appuser

# Install Python dependencies
COPY --chown=appuser:appuser requirements.txt .
RUN pip install --user --upgrade pip \
    && pip install --user -r requirements.txt

# Copy project files
COPY --chown=appuser:appuser . .

# Add local bin to PATH
ENV PATH="/app/.local/bin:${PATH}"

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose the port
EXPOSE ${PORT}

# Run gunicorn
CMD gunicorn ubteb_system.wsgi:application --bind 0.0.0.0:${PORT}
