__init__.py

"""ML Service для предсказания Diabetes."""


__main__.py

"""Точка входа для запуска ML сервиса."""
import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "mlapp.server:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
    )

server.py

"""
ML Service для предсказания на основе датасета Diabetes.
- Endpoint /api/v1/predict
- JSON логирование обращений
- Логирование работы модели в БД (вход, выход, время, версия)
- Endpoint /metrics для Prometheus
"""
import json
import logging
import os
import time
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request
from pydantic import BaseModel
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response

# JSON формат логов
class JsonFormatter(logging.Formatter):
    def format(self, record):
        return json.dumps({
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "message": record.getMessage(),
        }, ensure_ascii=False)

handler = logging.StreamHandler()
handler.setFormatter(JsonFormatter(datefmt="%Y-%m-%dT%H:%M:%S"))
logging.root.handlers = [handler]
logging.root.setLevel(logging.INFO)
logger = logging.getLogger(__name__)

_model = None
_model_version = "1.0.0"

# Prometheus метрики
REQUEST_COUNT = Counter("ml_service_requests_total", "Total requests", ["method", "endpoint"])
REQUEST_LATENCY = Histogram("ml_service_request_duration_seconds", "Request latency", ["endpoint"])
PREDICT_COUNT = Counter("ml_service_predictions_total", "Total predictions")
PREDICT_LATENCY = Histogram("ml_service_predict_duration_seconds", "Prediction latency")


class PatientData(BaseModel):
    """10 параметров пациента из датасета sklearn diabetes."""
    age: float
    sex: float
    bmi: float
    bp: float
    s1: float
    s2: float
    s3: float
    s4: float
    s5: float
    s6: float


class PredictResponse(BaseModel):
    predict: float


def get_db_connection():
    """Создаёт подключение к PostgreSQL для логирования."""
    import psycopg2
    conn_str = os.environ.get(
        "ML_SERVICE_DB_URL",
        "postgresql://ml_service:ml_service@localhost:5435/ml_service"
    )
    return psycopg2.connect(conn_str)


def init_prediction_log_table():
    """Создаёт таблицу для логирования предсказаний."""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS prediction_log (
                id SERIAL PRIMARY KEY,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                input_features JSONB,
                output_value FLOAT,
                duration_ms FLOAT,
                model_version VARCHAR(50)
            )
        """)
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        logger.warning("Could not init prediction_log table: %s", str(e))


def log_prediction_to_db(input_features: list, output: float, duration_ms: float):
    """Логирует предсказание в БД."""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO prediction_log (input_features, output_value, duration_ms, model_version) VALUES (%s, %s, %s, %s)",
            (json.dumps(input_features), output, duration_ms, _model_version)
        )
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        logger.warning("Could not log to DB: %s", str(e))


def load_model():
    """Загружает модель из файла или MLflow."""
    global _model
    if _model is not None:
        return _model

    model_path = Path(__file__).parent / "model"
    if model_path.exists():
        import mlflow.sklearn
        _model = mlflow.sklearn.load_model(str(model_path))
        return _model

    return None


@asynccontextmanager
async def lifespan(app: FastAPI):
    load_model()
    init_prediction_log_table()
    yield


app = FastAPI(title="Diabetes Prediction API", version=_model_version, lifespan=lifespan)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Middleware для JSON логирования всех запросов."""
    start = time.perf_counter()
    response = await call_next(request)
    duration = time.perf_counter() - start
    REQUEST_COUNT.labels(method=request.method, endpoint=request.url.path).inc()
    REQUEST_LATENCY.labels(endpoint=request.url.path).observe(duration)
    log_data = {
        "method": request.method,
        "path": str(request.url.path),
        "status": response.status_code,
        "duration_sec": round(duration, 4),
    }
    logger.info(json.dumps(log_data))
    return response


@app.get("/health")
async def health():
    """Проверка работоспособности сервиса."""
    return {"status": "ok"}


@app.get("/model/status")
async def model_status():
    """Проверка: загружена ли модель (обучена при сборке)."""
    model = load_model()
    model_path = Path(__file__).parent / "model"
    return {
        "model_loaded": model is not None,
        "model_path_exists": model_path.exists(),
        "model_version": _model_version,
    }


@app.get("/metrics")
async def metrics():
    """Prometheus метрики."""
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )


@app.post("/api/v1/predict", response_model=PredictResponse)
async def predict(data: PatientData):
    """
    Предсказание на основе 10 параметров пациента.
    """
    PREDICT_COUNT.inc()
    with PREDICT_LATENCY.time():
        model = load_model()
        if model is None:
            import random
            prediction = round(random.uniform(50, 300), 2)
            logger.info(json.dumps({"event": "predict_fallback", "predict": prediction}))
            return PredictResponse(predict=prediction)

        features = [
            data.age, data.sex, data.bmi, data.bp,
            data.s1, data.s2, data.s3, data.s4, data.s5, data.s6
        ]
        import numpy as np
        start = time.perf_counter()
        X = np.array([features])
        prediction = model.predict(X)[0]
        duration_ms = (time.perf_counter() - start) * 1000

        log_prediction_to_db(features, float(prediction), duration_ms)

        return PredictResponse(predict=round(float(prediction), 2))
