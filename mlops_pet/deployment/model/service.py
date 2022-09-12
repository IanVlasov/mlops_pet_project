from mlops_pet.deployment.model import utils


class ModelService:
    def __init__(self, model, model_version=None, callbacks=None):
        self.model = model
        self.model_version = model_version
        self.callbacks = callbacks or []

    def prepare_features(self, ride):
        features = {}
        features["PU_DO"] = f"{ride['PULocationID']}_{ride['DOLocationID']}"
        features["trip_distance"] = ride["trip_distance"]
        return features

    def predict(self, features):
        pred = self.model.predict(features)
        return float(pred[0])

    def lambda_handler(self, event):
        # print(json.dumps(event))

        predictions_events = []

        for record in event["Records"]:
            encoded_data = record["kinesis"]["data"]
            ride_event = utils.base64_decode(encoded_data)

            # print(ride_event)
            ride = ride_event["ride"]
            ride_id = ride_event["ride_id"]

            features = self.prepare_features(ride)
            prediction = self.predict(features)

            prediction_event = {
                "model": "ride_duration_prediction_model",
                "version": self.model_version,
                "prediction": {"ride_duration": prediction, "ride_id": ride_id},
            }

            for callback in self.callbacks:
                callback(prediction_event)

            predictions_events.append(prediction_event)

        return {"predictions": predictions_events}
