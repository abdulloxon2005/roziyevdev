# ==============================================================================
# ROZIYEVDEV — PRODUCTION DOCKERFILE
# ==============================================================================
FROM python:3.11-slim

# Muhit o'zgaruvchilari
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Tizim paketlarini o'rnatish
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Python kutubxonalarini o'rnatish
COPY requirements.txt /app/
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Loyiha kodini ko'chirish
COPY . /app/

# Media va statik papkalarni tayyorlash
RUN mkdir -p /app/staticfiles /app/media

EXPOSE 8000

# Gunicorn orqali ishga tushirish
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "--timeout", "300", "config.wsgi:application"]
