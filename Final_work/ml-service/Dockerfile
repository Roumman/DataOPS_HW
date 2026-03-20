FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY mlapp/ ./mlapp/
COPY scripts/ ./scripts/

RUN python scripts/train_local.py

EXPOSE 8000

CMD ["python", "-m", "mlapp"]
