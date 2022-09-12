import os
from pathlib import Path

# GENERAL
PROJECT_ROOT = Path(__file__).parent
TESTS_ROOT = Path(__file__).parent / ".." / "tests"

TEST_RUN = False

# AWS
AWS_ACCESS_KEY_ID = "minio" if TEST_RUN else os.getenv("AWS_ACCESS_KEY_ID", "minio")
AWS_SECRET_ACCESS_KEY = "minio123" if TEST_RUN else os.getenv("AWS_SECRET_ACCESS_KEY", "minio123")
# MLFLOW
MLFLOW_S3_ENDPOINT_URL = (
    "http://0.0.0.0:9000"
    if TEST_RUN
    else os.getenv("MLFLOW_S3_ENDPOINT_URL", "http://0.0.0.0:9000")
)
MLFLOW_TRACKING_URI = (
    "http://0.0.0.0:5001/" if TEST_RUN else os.getenv("MLFLOW_TRACKING_URI", "http://0.0.0.0:5001/")
)
MLFLOW_PORT = "5001" if TEST_RUN else os.getenv("MLFLOW_PORT", "5001")
EXPERIMENT_NAME = "fare_prediction" if TEST_RUN else os.getenv("EXPERIMENT_NAME", "fare_prediction")
MODEL_NAME = (
    "fare_prediction_model" if TEST_RUN else os.getenv("MODEL_NAME", "fare_prediction_model")
)

# PREFECT
PREFECT_API_URL = (
    "http://0.0.0.0:4201/api"
    if TEST_RUN
    else os.getenv("PREFECT_API_URL", "http://0.0.0.0:4201/api")
)
PREFECT_PORT = "4201" if TEST_RUN else os.getenv("PREFECT_PORT", "4201")

# KINESIS
KINESIS_ENDPOINT_URL = os.getenv("KINESIS_ENDPOINT_URL", "")
PREDICTIONS_STREAM_NAME = (
    "fare_predictions" if TEST_RUN else os.getenv("PREDICTIONS_STREAM_NAME", "fare_predictions")
)


def set_env():
    os.environ["AWS_ACCESS_KEY_ID"] = AWS_ACCESS_KEY_ID
    os.environ["AWS_SECRET_ACCESS_KEY"] = AWS_SECRET_ACCESS_KEY
    os.environ["MLFLOW_S3_ENDPOINT_URL"] = MLFLOW_S3_ENDPOINT_URL
    os.environ["MLFLOW_TRACKING_URI"] = MLFLOW_TRACKING_URI
    os.environ["MLFLOW_PORT"] = MLFLOW_PORT
    os.environ["EXPERIMENT_NAME"] = EXPERIMENT_NAME
    os.environ["PREFECT_API_URL"] = PREFECT_API_URL
    os.environ["PREFECT_PORT"] = PREFECT_PORT
    os.environ["KINESIS_ENDPOINT_URL"] = KINESIS_ENDPOINT_URL
    os.environ["PREDICTIONS_STREAM_NAME"] = PREDICTIONS_STREAM_NAME
