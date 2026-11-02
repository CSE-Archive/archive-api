# CSE Archive API — production image.
# Python 3.10 matches Pipfile [requires]; every version pin comes from
# Pipfile.lock (rendered to requirements.lock — the repo's Pipfile/Pipfile.lock
# are out of sync with each other, so `pipenv install --deploy` refuses to run).
FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# gcc + libc6-dev + libpq-dev: psycopg2 2.9.8 builds from source (the lock
# pins `psycopg2`, not the -binary variant). libpq-dev also provides runtime
# libpq.
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libc6-dev libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# --timeout/--retries: PyPI transit can be slow from some networks; don't
# give up early.
COPY requirements.lock ./
RUN pip install --no-cache-dir --timeout 60 --retries 10 -r requirements.lock

COPY . .

# Entrypoint: static files into STATIC_ROOT (whitenoise serves them), then
# migrate (idempotent), then hand over to gunicorn.
CMD ["sh", "-c", "python manage.py collectstatic --noinput && python manage.py migrate --noinput && exec gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 2 --threads 4 --timeout 120 --access-logfile - --error-logfile -"]
