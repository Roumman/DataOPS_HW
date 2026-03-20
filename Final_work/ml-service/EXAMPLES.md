# Примеры запросов к ML-сервису

## Health check
```bash
curl http://localhost:8003/health
```

## Проверка модели (обучилась ли при сборке)
```bash
curl http://localhost:8003/model/status
```
Ожидаемый ответ: `{"model_loaded": true, "model_path_exists": true, "model_version": "1.0.0"}`

## Predict
```bash
curl -X POST http://localhost:8003/api/v1/predict \
  -H "Content-Type: application/json" \
  -d '{
    "age": 0.04,
    "sex": 0.05,
    "bmi": 0.06,
    "bp": 0.07,
    "s1": 0.08,
    "s2": 0.09,
    "s3": 0.1,
    "s4": 0.11,
    "s5": 0.12,
    "s6": 0.13
  }'
```

## Prometheus metrics
```bash
curl http://localhost:8003/metrics
```
