"""
ML Service для предсказания на основе датасета Diabetes.
Endpoint /api/v1/predict принимает 10 параметров пациента и возвращает предсказание.
"""
from pathlib import Path

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Diabetes Prediction API", version="1.0.0")

# Глобальная переменная для модели (загружается при старте)
_model = None


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

    # Fallback: модель не загружена (для разработки без модели)
    return None


@app.on_event("startup")
async def startup_event():
    """Загрузка модели при старте сервиса."""
    load_model()


@app.get("/health")
async def health():
    """Проверка работоспособности сервиса."""
    return {"status": "ok"}


@app.post("/api/v1/predict", response_model=PredictResponse)
async def predict(data: PatientData):
    """
    Предсказание на основе 10 параметров пациента.
    Параметры соответствуют датасету sklearn.datasets.load_diabetes.
    """
    model = load_model()
    if model is None:
        # Fallback: случайное значение для разработки без модели
        import random
        return PredictResponse(predict=round(random.uniform(50, 300), 2))

    features = [
        data.age, data.sex, data.bmi, data.bp,
        data.s1, data.s2, data.s3, data.s4, data.s5, data.s6
    ]
    import numpy as np
    X = np.array([features])
    prediction = model.predict(X)[0]
    return PredictResponse(predict=round(float(prediction), 2))
