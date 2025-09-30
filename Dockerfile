# Frontend build stage
FROM node:18 AS frontend-builder
WORKDIR /frontend

COPY client/package*.json ./
RUN npm ci

COPY client/ ./
RUN npm run build

# Final runtime image
FROM mcr.microsoft.com/playwright/python:v1.41.1-jammy

WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends git \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu \
    && pip install --no-cache-dir -r requirements.txt \
    && playwright install --with-deps chromium

COPY docker-entrypoint.sh ./
RUN chmod +x docker-entrypoint.sh

COPY --from=frontend-builder /frontend/dist ./client_dist
COPY . ./

ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000
ENV FLASK_ENV=production

EXPOSE 5000

ENTRYPOINT ["./docker-entrypoint.sh"]
CMD ["python", "app.py"]