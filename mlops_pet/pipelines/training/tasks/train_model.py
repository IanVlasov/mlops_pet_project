from __future__ import annotations

import hyperopt
import mlflow
from hyperopt import hp, tpe
from hyperopt.pyll import scope
from numpy import typing as npt
from prefect import task
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.linear_model import Lasso, Ridge
from sklearn.metrics import mean_squared_error

SEARCH_SPACE = hp.choice(
    "regressor_type",
    [
        {"type": "Ridge", "alpha": hp.quniform("alpha_ridge", 0, 2, 0.2)},
        {"type": "Lasso", "alpha": hp.quniform("alpha_lasso", 0, 2, 0.2)},
        {
            "type": "GradientBoostingRegressor",
            "learning_rate": hp.choice("learning_rate", [0.1, 0.2, 0.5]),
            "n_estimators": scope.int(hp.quniform("n_estimators", 5, 10, 1)),
        },
    ],
)


@task
def train_model(
    x_train: npt.ArrayLike,
    x_test: npt.ArrayLike,
    y_train: npt.ArrayLike,
    y_test: npt.ArrayLike,
    num_trials: int = 5,
    random_state: int | None = None,
) -> None:
    def objective(params):
        with mlflow.start_run():
            reg_type = params["type"]
            mlflow.set_tag("model", reg_type)
            mlflow.log_params(params)
            del params["type"]
            if reg_type == "Lasso":
                regressor = Lasso(**params)
            elif reg_type == "Ridge":
                regressor = Ridge(**params)
            elif reg_type == "GradientBoostingRegressor":
                regressor = GradientBoostingRegressor(**params)
            else:
                return 0
            regressor.fit(x_train, y_train)

            y_predict = regressor.predict(x_test)
            rmse = mean_squared_error(y_test, y_predict, squared=False)
            mlflow.log_metric("rmse", rmse)
            mlflow.sklearn.log_model(regressor, artifact_path="model")

        return {"loss": rmse, "status": hyperopt.STATUS_OK}

    hyperopt.fmin(
        fn=objective,
        space=SEARCH_SPACE,
        algo=tpe.suggest,
        max_evals=num_trials,
        trials=hyperopt.Trials(),
        rstate=random_state,
    )
