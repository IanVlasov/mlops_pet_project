# pylint: disable=duplicate-code

import json

import requests
from deepdiff import DeepDiff


def test_lambda():
    with open("event.json", encoding="utf-8") as f_in:
        event = json.load(f_in)

    url = "http://localhost:8080/2015-03-31/functions/function/invocations"
    actual_response = requests.post(url, json=event, timeout=30).json()
    print("actual response:")

    print(json.dumps(actual_response, indent=2))

    expected_response = {
        "predictions": [
            {
                "version": "fare_prediction_model",
                "prediction": {
                    "fare_prediction": 12.86,
                    "ride_id": 256,
                },
            }
        ]
    }

    diff = DeepDiff(
        actual_response,
        expected_response,
        exclude_paths={"root['predictions'][0]['prediction']['fare_prediction']"},
    )
    print(f"diff={diff}")

    assert "type_changes" not in diff
    assert "values_changed" not in diff


if __name__ == "__main__":
    test_lambda()
