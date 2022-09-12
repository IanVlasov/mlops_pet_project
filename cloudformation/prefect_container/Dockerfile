FROM --platform=linux/amd64 python:3.8.0

RUN pip install \
    prefect \
    greenlet

EXPOSE ${PREFECT_PORT}

RUN prefect config set PREFECT_ORION_UI_API_URL="http://${EXTERNAL_URL}:${PREFECT_PORT}/api"

CMD prefect orion start \
    --host 0.0.0.0 \
    --port=${PREFECT_PORT}
