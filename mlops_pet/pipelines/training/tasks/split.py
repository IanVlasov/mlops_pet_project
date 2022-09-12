from __future__ import annotations

import pandas as pd
from numpy import typing as npt
from prefect import task
from sklearn.model_selection import train_test_split


@task
def split(
    data: pd.DataFrame, targets: pd.Series, test_size: float = 0.3, **kwargs
) -> tuple[npt.ArrayLike, npt.ArrayLike, npt.ArrayLike, npt.ArrayLike]:
    x_train, x_test, y_train, y_test = train_test_split(
        data, targets, test_size=test_size, **kwargs
    )
    return x_train, x_test, y_train, y_test
