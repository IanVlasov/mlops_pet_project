import base64
import json
import os

import boto3
import mlflow

mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI"))


def load_model(model_name: str, stage: str = "Production"):
    model_uri = f"models:/{model_name}/{stage}"
    model = mlflow.pyfunc.load_model(model_uri)
    return model


def base64_decode(encoded_data):
    decoded_data = base64.b64decode(encoded_data).decode("utf-8")
    ride_event = json.loads(decoded_data)
    return ride_event


def create_kinesis_client():
    endpoint_url = os.getenv("KINESIS_ENDPOINT_URL")
    if endpoint_url is None:
        return boto3.client("kinesis")
    return boto3.client("kinesis", endpoint_url=endpoint_url)
