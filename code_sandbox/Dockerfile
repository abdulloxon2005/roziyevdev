# ==============================================================================
# ROZIYEVDEV — PYTHON KOD SANDBOX XIZMATI
# Faqat standart kutubxona. Root bo'lmagan foydalanuvchi, loyiha kodi va maxfiy
# kalitlarsiz. Tarmoq/FS/resurs cheklovlari docker-compose.yml da beriladi.
# ==============================================================================
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN useradd --uid 10001 --no-create-home --shell /usr/sbin/nologin sandbox

WORKDIR /srv
COPY code_sandbox/ /srv/code_sandbox/

USER sandbox
EXPOSE 8080

CMD ["python", "-m", "code_sandbox.server", "--host", "0.0.0.0", "--port", "8080"]
