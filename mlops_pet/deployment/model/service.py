import os
from datetime import datetime

from pandas import DataFrame

from mlops_pet.deployment.model import utils


class ModelService:
    def __init__(self, model, model_version=None, callbacks=None):
        self.model = model
        self.model_version = model_version
        self.callbacks = callbacks or []

    def predict(self, features):
        pred = self.model.predict(features)
        return float(pred[0])

    def lambda_handler(self, event):
        predictions_events = []

        for record in event["Records"]:
            encoded_data = record["kinesis"]["data"]
            ride_event = utils.base64_decode(encoded_data)
            ride = ride_event["ride"]
            ride_id = ride_event["ride_id"]

            features = _prepare_features(ride)
            prediction = self.predict(features)

            prediction_event = {
                "version": self.model_version,
                "prediction": {"fare_prediction": prediction, "ride_id": ride_id},
            }

            for callback in self.callbacks:
                callback(prediction_event)

            predictions_events.append(prediction_event)

        return {"predictions": predictions_events}


def _prepare_features(ride):
    features = {}
    pickup_time = datetime.fromisoformat(ride["pickup_datetime"])

    features["passenger_count"] = [ride["passenger_count"]]
    features["trip_distance"] = [ride["trip_distance"]]
    features["pickup_hour"] = [pickup_time.hour]
    features["pickup_minutes"] = [pickup_time.minute]
    features["weekday"] = [pickup_time.weekday()]
    return DataFrame.from_dict(features)
