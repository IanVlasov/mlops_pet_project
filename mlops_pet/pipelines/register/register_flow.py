import mlflow
from mlflow.entities import ViewType
from mlflow.exceptions import MlflowException
from prefect import flow, task_runners

from mlops_pet import definitions


@flow(task_runner=task_runners.SequentialTaskRunner(), name="register_best_model_flow")
def main():
    client = mlflow.MlflowClient(definitions.MLFLOW_TRACKING_URI)
    experiment = client.get_experiment_by_name(definitions.EXPERIMENT_NAME)
    best_run = client.search_runs(
        experiment_ids=experiment.experiment_id,
        run_view_type=ViewType.ACTIVE_ONLY,
        max_results=1,
        order_by=["metrics.rmse DESC"],
    )[0]

    model_uri = f"runs:/{best_run.info.run_id}/model"
    _ = mlflow.register_model(model_uri, definitions.MODEL_NAME)

    try:
        _ = mlflow.pyfunc.load_model(model_uri=f"models:/{definitions.MODEL_NAME}/Production")
    except MlflowException:
        mv = client.create_model_version(
            definitions.MODEL_NAME,
            model_uri,
            best_run.info.run_id,
        )
        client.transition_model_version_stage(
            definitions.MODEL_NAME, mv.version, stage="Production"
        )
