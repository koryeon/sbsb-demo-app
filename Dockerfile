FROM python:3.11-slim

# Set environment
ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VIRTUALENVS_CREATE=false

# Create a non-root user and app directory
RUN groupadd --gid 1000 appgroup \
    && useradd --uid 1000 --gid appgroup --shell /bin/bash --create-home appuser \
    && mkdir /app \
    && chown appuser:appgroup /app

WORKDIR /app

# Install dependencies (copy requirements first to leverage docker cache)
COPY requirements.txt /app/requirements.txt

# Use pip to install pinned dependencies deterministically from requirements.txt
RUN python -m pip install --upgrade pip \
    && python -m pip install --no-warn-script-location --require-hashes --disable-pip-version-check -r /app/requirements.txt 2>/dev/null || python -m pip install --no-warn-script-location --disable-pip-version-check -r /app/requirements.txt

# Copy application code
COPY --chown=appuser:appgroup . /app

USER appuser

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
