import os

import typer

from mlops_pet import __version__ as mlops_pet_version
from mlops_pet import definitions, pipelines

app = typer.Typer(add_completion=False, help="MLOps-pet CLI interface", no_args_is_help=True)


def version_callback(value: bool):
    """Function that will return version of the Qflow package."""
    if value:
        print(f"Qflow CLI Version: {mlops_pet_version}")
        raise typer.Exit(code=0)


@app.callback()
def common(
    ctx: typer.Context,
    version: bool = typer.Option(None, "--version", "-V", callback=version_callback),
):
    """Empty callback to allow `-v` and `--version` options usage."""


@app.command(help="Setup the environment variables for the project")
def setup(
    aws_access_key_id: str = typer.Option("minio", prompt="AWS ACCESS KEY ID"),
    aws_secret_access_key: str = typer.Option("minio123", prompt="AWS SECRET ACCESS KEY"),
    mlflow_s3_endpoint_url: str = typer.Option(
        "http://0.0.0.0:9000", prompt="MLFLOW S3 ENDPOINT URL"
    ),
    mlflow_tracking_uri: str = typer.Option("http://0.0.0.0:5001/", prompt="MLFlow Tracking URI"),
    mlflow_port: str = typer.Option("5001", prompt="MLFlow Port"),
    mlflow_experiment_name: str = typer.Option("fare_prediction", prompt="MLFlow experiment name"),
    prefect_api_url: str = typer.Option("http://0.0.0.0:4201/api", prompt="Prefect API URL"),
    prefect_port: str = typer.Option("4201", prompt="Prefect Port"),
    kinesis_endpoint_uri: str = typer.Option("", prompt="Kinesis Endpoint URL"),
    prediction_stream_name: str = typer.Option("fare_predictions", prompt="Prediction Stream Name"),
):
    os.system(f"export AWS_ACCESS_KEY_ID = {aws_access_key_id}")
    os.system(f"export AWS_SECRET_ACCESS_KEY = {aws_secret_access_key}")
    os.system(f"export MLFLOW_S3_ENDPOINT_URL = {mlflow_s3_endpoint_url}")
    os.system(f"export MLFLOW_TRACKING_URI = {mlflow_tracking_uri}")
    os.system(f"export MLFLOW_PORT = {mlflow_port}")
    os.system(f"export EXPERIMENT_NAME = {mlflow_experiment_name}")
    os.system(f"export PREFECT_API_URL = {prefect_api_url}")
    os.system(f"export PREFECT_PORT = {prefect_port}")
    os.system(f"export KINESIS_ENDPOINT_URL = {kinesis_endpoint_uri}")
    os.system(f"export PREDICTIONS_STREAM_NAME = {prediction_stream_name}")


@app.command(help="Run training pipeline")
def train(
    date: str = typer.Option(
        "2022-01-01",
        prompt="Date in ISO format",
        help="Date to collect training data for particular period",
    ),
    num_trials: int = typer.Option(5, prompt="Number of trials for HyperOpt"),
    test: bool = typer.Option(False, help="Use it to run a local test run"),
):
    definitions.TEST_RUN = test
    definitions.set_env()
    pipelines.training_flow(date=date, num_trials=num_trials)


@app.command(help="Register best model from existing runs based on the lowest RMSE value.")
def register_best_model(
    test: bool = typer.Option(False, help="Use it to run a local test run"),
):
    definitions.TEST_RUN = test
    definitions.set_env()
    pipelines.register_flow()


def main():
    """Main Entry Point."""
    app()
