from typing import Optional

from datetime import datetime

import mlflow
from prefect import flow, task_runners

from mlops_pet import definitions
from mlops_pet.pipelines.training import tasks


@flow(task_runner=task_runners.SequentialTaskRunner(), name="training_flow")
def main(
    date: Optional[str] = None,
    num_trials: int = 5,
):
    mlflow.set_tracking_uri(definitions.MLFLOW_TRACKING_URI)
    mlflow.set_experiment(definitions.EXPERIMENT_NAME)

    if date is None:
        date = datetime.today()
    else:
        date = datetime.fromisoformat(date)

    month = date.month
    year = date.year

    features, targets = tasks.preprocess_data(year=year, month=month)
    x_train, x_test, y_train, y_test = tasks.split(
        data=features, targets=targets, random_state=definitions.RANDOM_STATE
    )
    tasks.train_model(
        x_train,
        x_test,
        y_train,
        y_test,
        num_trials=num_trials,
        random_state=definitions.RANDOM_STATE,
    )
