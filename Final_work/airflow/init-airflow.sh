#!/bin/bash
# Инициализация Airflow (если airflow-init не сработал)
# Логин по умолчанию: airflow / airflow

set -e
echo "Creating airflow user..."
docker compose run --rm airflow-webserver airflow users create \
  --username airflow \
  --firstname Admin \
  --lastname User \
  --role Admin \
  --email admin@example.com \
  --password airflow || true

echo "Done! Login: airflow / airflow"
