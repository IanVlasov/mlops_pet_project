from __future__ import annotations

import pandas as pd
from prefect import task


@task
def preprocess_data(year: str, month: str) -> tuple[pd.DataFrame, pd.Series]:
    data_uri = (
        "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_"
        f"{year:04d}-{month:02d}.parquet"
    )
    data = pd.read_parquet(data_uri)

    targets = data.fare_amount.copy()
    features = pd.DataFrame(data["passenger_count"].copy())
    features.passenger_count.fillna(1, inplace=True)
    features["pickup_hour"] = data["tpep_pickup_datetime"].dt.hour
    features["pickup_minutes"] = data["tpep_pickup_datetime"].dt.minute
    features["weekday"] = data["tpep_pickup_datetime"].dt.weekday

    return features, targets
