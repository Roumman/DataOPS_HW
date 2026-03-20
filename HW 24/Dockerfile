FROM python:3.11-slim

WORKDIR /app

# Копируем зависимости
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходники сервиса и скрипт обучения
COPY mlapp/ ./mlapp/
COPY scripts/ ./scripts/

# Обучаем модель при сборке (альтернатива: выполнить research/train.ipynb с MLflow)
RUN python scripts/train_local.py

EXPOSE 8000

CMD ["python", "-m", "mlapp"]
