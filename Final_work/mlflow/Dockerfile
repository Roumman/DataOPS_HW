FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir mlflow psycopg2-binary

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 5000

ENTRYPOINT ["/entrypoint.sh"]
