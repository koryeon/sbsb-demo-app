FROM python:3.11-slim

# Metadata
LABEL org.opencontainers.image.title="sbsb-demo-fastapi"
LABEL org.opencontainers.image.source="."

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    APP_HOME=/app \
    PORT=8000

# Create non-root user and application directory
RUN groupadd --gid 1000 appgroup \
    && useradd --uid 1000 --gid appgroup --shell /usr/sbin/nologin --create-home app \
    && mkdir -p ${APP_HOME} \
    && chown app:appgroup ${APP_HOME}

WORKDIR ${APP_HOME}

# Install build dependencies, install python deps, then remove build deps to keep image small
# Use deterministic installation from requirements.txt
COPY requirements.txt ./

RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libpq-dev build-essential \
    && pip install --no-cache-dir --upgrade pip setuptools wheel \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get remove -y --purge gcc build-essential \
    && apt-get autoremove -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy application code
COPY --chown=app:appgroup . .

USER app

EXPOSE 8000

# Run the app binding to 0.0.0.0
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--lifespan", "on"]
