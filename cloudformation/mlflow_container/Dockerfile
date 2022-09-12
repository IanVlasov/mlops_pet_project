FROM --platform=linux/amd64 python:3.8.0

RUN pip install \
    mlflow \
    psycopg2 \
    pymysql \
    cryptography \
    boto3 && \
    mkdir /mlflow/

EXPOSE ${MLFLOW_PORT}

CMD mlflow server \
    --host 0.0.0.0 \
    --port ${MLFLOW_PORT} \
    --default-artifact-root ${BUCKET} \
    --backend-store-uri postgresql://${USERNAME}:${PASSWORD}@${HOST}:${PORT}/${DATABASE}
