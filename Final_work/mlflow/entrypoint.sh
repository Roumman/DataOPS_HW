#!/bin/sh
set -e
BACKEND_URI="postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@db:5432/${POSTGRES_DB}"
exec mlflow server \
  --host 0.0.0.0 \
  --port 5000 \
  --backend-store-uri "$BACKEND_URI" \
  --default-artifact-root /mlflow/artifacts
