# Backend Dockerfile
FROM python:3.11-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# System deps for psycopg2
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Prefer IPv4 over IPv6 to avoid connection issues in networks without IPv6 routing
RUN sed -i 's/#precedence ::ffff:0:0\/96  100/precedence ::ffff:0:0\/96  100/' /etc/gai.conf || true

COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Set default DB to sqlite for build-time tests
ENV DATABASE_URL=sqlite:///./test.db

COPY . /app

# Run tests during build
RUN pytest -q

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
