
# Примеры вызовов API (curl)

## Запуск сервиса

```bash
cd DataOpsHSE/HW24
docker compose up --build
```

## Вызов 1

```bash
curl -X POST http://localhost:8000/api/v1/predict \
  -H "Content-Type: application/json" \
  -d '{"age": 0.04, "sex": 0.05, "bmi": 0.06, "bp": 0.07, "s1": 0.08, "s2": 0.09, "s3": 0.1, "s4": 0.11, "s5": 0.12, "s6": 0.13}'
```

## Вызов 2

```bash
curl -X POST http://localhost:8000/api/v1/predict \
  -H "Content-Type: application/json" \
  -d '{"age": -0.1, "sex": -0.05, "bmi": 0.0, "bp": 0.02, "s1": -0.01, "s2": 0.03, "s3": 0.04, "s4": -0.02, "s5": 0.01, "s6": 0.0}'
```

## Вызов 3

```bash
curl -X POST http://localhost:8000/api/v1/predict \
  -H "Content-Type: application/json" \
  -d '{"age": 0.15, "sex": 0.1, "bmi": 0.2, "bp": 0.18, "s1": 0.12, "s2": 0.14, "s3": 0.16, "s4": 0.1, "s5": 0.2, "s6": 0.15}'
```

## Health check

```bash
curl http://localhost:8000/health
```
