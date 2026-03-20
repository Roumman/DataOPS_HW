### 1. MLflow (порт 5001)
```bash
cd mlflow && docker compose up -d
# UI: http://localhost:5001
# Создать промпты: pip install mlflow && MLFLOW_TRACKING_URI=http://localhost:5001 python scripts/create_prompts.py
```

### 2. Airflow (порт 8080)
```bash
cd airflow
docker compose up -d
# airflow-init создаст пользователя автоматически
# UI: http://localhost:8080
# Логин: airflow / airflow
```

**Если не получается залогиниться** — сбросить и пересоздать:
```bash
docker compose down --volumes
docker compose up -d
# Или вручную: docker compose run --rm airflow-webserver airflow users create --username airflow --firstname Admin --lastname User --role Admin --email admin@example.com --password airflow
```

### 3. LakeFS (порт 8001)
```bash
cd lakefs && docker compose up -d
# UI: http://localhost:8001
# MinIO: http://localhost:9001
# Создать репозиторий в UI, ветку, добавить файл, commit
```

### 4. JupyterHub (порт 8002)
```bash
cd jupyterhub && docker compose up -d
# UI: http://localhost:8002
# Логин: admin (DummyAuthenticator — любой пароль)
```

### 5. ML-сервис (порт 8003)
```bash
cd ml-service && docker compose up -d
# API: http://localhost:8003
# Health: http://localhost:8003/health
# Predict: POST http://localhost:8003/api/v1/predict
# Metrics: http://localhost:8003/metrics
```

### 6. Мониторинг (Prometheus 9090, Grafana 3000)
```bash
# Вариант A: ML-сервис + мониторинг вместе
docker compose -f docker-compose.full.yaml up -d

# Вариант B: Отдельно (ML-сервис на 8003, prometheus на host.docker.internal:8003)
cd monitoring && docker compose up -d
```

Grafana: http://localhost:3000 (admin/admin)
Добавить источник: Prometheus, URL: http://prometheus:9090

### 7. Kubernetes
```bash
# Собрать образ
docker build -t ml-service:1.0.0 ml-service/

# Деплой (требуется кластер)
kubectl apply -f k8s/
```

### 8. Helm
```bash
helm install ml-service ./helm/ml-service
# С версией образа: helm install ml-service ./helm/ml-service --set image.tag=2.0.0
# С ресурсами: helm install ml-service ./helm/ml-service --set resources.requests.memory=512Mi
```

### 9. MLflow Prompt Storage
```bash
cd mlflow
pip install mlflow
python scripts/create_prompts.py
# Проверить в UI: http://localhost:5001 -> Prompts
```

## Пример запроса к ML-сервису

```bash
curl -X POST http://localhost:8003/api/v1/predict \
  -H "Content-Type: application/json" \
  -d '{"age":0.04,"sex":0.05,"bmi":0.06,"bp":0.07,"s1":0.08,"s2":0.09,"s3":0.1,"s4":0.11,"s5":0.12,"s6":0.13}'
```

## Порты

| Сервис    | Порт |
|-----------|------|
| MLflow    | 5001 |
| Airflow   | 8080 |
| LakeFS    | 8001 |
| MinIO     | 9000, 9001 |
| JupyterHub| 8002 |
| ML-сервис | 8003 |
| Prometheus| 9090 |
| Grafana   | 3000 |
