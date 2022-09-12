from mlops_pet import definitions
from mlops_pet.deployment.model import utils


def test_base64_decode():
    test_file = definitions.TESTS_ROOT / "resources" / "data.b64"

    with open(test_file, encoding="utf-8") as f_in:
        base64_input = f_in.read().strip()

    result = utils.base64_decode(base64_input)
    expected = {
        "ride": {
            "passenger_count": 1,
            "trip_distance": 3.66,
            "pickup_datetime": "2022-01-01 09:15:00",
        },
        "ride_id": 256,
    }

    assert result == expected
